from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import models as auth_models
from Aplicaciones.Modelos.estados import ESTADO_PUBLICACION, ESTADO_OFERTA, ESTADO_INTERCAMBIO

# ---------- USUARIOS ---------------------------------------------------------------------------

class Usuario(auth_models.AbstractUser):
    #Se usa campo password de la clase AbstractUser
    dni = models.IntegerField( validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ], unique=True)
    fecha_nacimiento = models.DateField()

    #campos para el bloqueo de cuenta
    bloqueado = models.BooleanField(default=False)
    contador_ingresos_fallidos = models.IntegerField(default=0)
    fecha_bloqueo = models.DateTimeField(null=True)

    #Especifico nombres y Permisos Unicos para no entrar en conflicto con el modelo auth.User integrado de Django
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='mis_usuarios_personalizados', #related_name entraba en conflicto porque creaba un user auth con mismo nombre
        blank=True,
        help_text='Los grupos a los que pertenece el usuario',
        verbose_name='grupos',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='mis_permisos_personalizados', 
        blank=True,
        help_text='Permisos específicos para este usuario.',
        verbose_name='permisos de usuario',
    )

    def incrementar_ingresos_fallidos(self):
        if not self.bloqueado and self.contador_ingresos_fallidos < 5:
            self.contador_ingresos_fallidos += 1
            self.save(update_fields=['contador_ingresos_fallidos']) #Actualizo campo
            if self.contador_ingresos_fallidos == 5: #Si los fallos llegaron a 5, bloqueo la cuenta
                    self.bloquear()

    def resetear_ingresos_fallidos(self):
        self.contador_ingresos_fallidos = 0
        self.save(update_fields=['contador_ingresos_fallidos'])

    def bloquear(self):
        self.bloqueado = True
        self.fecha_bloqueo = timezone.now() #Uso timezone.now() para guardar también hora,dia,minutos,segundos...
        self.save(update_fields=['bloqueado', 'fecha_bloqueo'])
        #raise ValidationError('Usuario o contraseña no validos. Por favor, intenta de nuevo')
    
    def desbloquear(self):
        self.bloqueado = False
        self.fecha_bloqueo = None
        self.resetear_ingresos_fallidos()
        self.save(update_fields=['bloqueado', 'fecha_bloqueo'])
    
    def cuanto_te_falta(self):
        ahora = timezone.now()
        fechaDeDesbloqueo = self.fecha_bloqueo + timedelta(minutes=2) #tremenda falopa, además de ser del mismo tipo, tenés que verificar que ambos datetime sean naive o aware
        tiempoRestante = (fechaDeDesbloqueo - ahora)
        return tiempoRestante.total_seconds()/3600
    
    class Meta:
        verbose_name = "Mi modelo de usuario"
        verbose_name_plural = "Mis modelos de usuario"


class Persona(models.Model):
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    
# ---------- PUBLICACIONES ----------------------------------------------------------------------

class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=1)
    tipo_embarcacion = models.CharField(max_length=60, choices=TIPOS_EMBARCACION)
    anio = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)])
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones')
    descripcion = models.CharField(max_length=150, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PUBLICACION, default='pendiente')
    oferta_aceptada = models.OneToOneField('Oferta', on_delete=models.SET_NULL, null=True, related_name='publicacion_ofertada')
    # Con el OneToOne cada publicacion puede tener como maximo una oferta aceptada, y cada oferta aceptada puede estar vinculada solo a una publicacion

    def aceptar_oferta(self, oferta):
        if oferta.estado == 'rechazada':
            raise Exception("No se puede aceptar una oferta rechazada.")
        if self.oferta_aceptada:
            raise Exception("Ya hay una oferta aceptada para esta publicación.")
        oferta.estado = 'aceptada'
        oferta.save()
        self.oferta_aceptada = oferta
        self.save()

    def rechazar_oferta(self, oferta):
        if oferta.estado == 'aceptada':
            raise Exception("No se puede rechazar una oferta que ya ha sido aceptada.")
        oferta.estado = 'rechazada'
        oferta.save()

    def cancelar_oferta_aceptada(self):
        if not self.oferta_aceptada:
            raise Exception("No hay oferta aceptada para cancelar.")
        self.oferta_aceptada.estado = 'cancelada'
        self.oferta_aceptada.save()
        self.oferta_aceptada = None
        self.save()


class FotoPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='archivos-estaticos/fotos_publicaciones/')
    """
    El upload es necesario porque sino las fotos se almacenan directamente en la base de datos como datos binarios,
    lo que puede hacerla más pesada y menos eficiente para recuperar y manejar
    """

# ---------- OFERTAS -----------------------------------------------------------------------------

class Oferta(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ofertas_autor')
    publicacion = models.ForeignKey(Publicacion, related_name='ofertas_publicacion', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=150)
    precio_estimado = models.DecimalField(max_digits=10, decimal_places=1)
    estado = models.CharField(max_length=10, choices=ESTADO_OFERTA, default='pendiente')


class FotoOferta(models.Model):
    oferta = models.ForeignKey(Oferta, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='archivos-estaticos/fotos_ofertas/', null=True, blank=True)


# ---------- INTERCAMBIOS -----------------------------------------------------------------------------
class Intercambios(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='intercambios', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_INTERCAMBIO, default='aceptado') # por que un intercambio esta aceptado x defecto??
    fecha_aceptacion = models.DateTimeField(default=now, null=True)


# ---------- CHAT --------------------------------------------------------------------------------------
class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(Usuario, through='RoomUser', related_name='roomsUser')

class RoomUser(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    unread_messages = models.BooleanField(default=False)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE)
    content = models.TextField()
    foto = models.ImageField(upload_to='archivos-estaticos/fotos_chats/', null=False) #POR EL MOMENTO NO ME ESTARÍA FUNCIONANDO EL TEMA DE LAS FOTOS
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta: #para guardar los mensajes ordenados por fecha
        ordering = ("date_added",)


   # ---------- NOTIFICACIONES --------------------------------------------------------------------------------------     

class Notificacion(models.Model):
    user = models.ForeignKey(Usuario,related_name="userN", on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=150, null=True, blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-fecha",)




