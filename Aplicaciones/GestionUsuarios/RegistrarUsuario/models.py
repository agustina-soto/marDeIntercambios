from datetime import timedelta
from django.contrib.auth import models as auth_models
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Usuario(auth_models.AbstractUser):
    #Se usa campo password de la clase AbstractUser
    # Campos adicionales

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