from django.db import models
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

from MDI import settings #se importa para manejar los permisos que puede tener un user 


class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    precio_minimo = models.DecimalField(max_digits=7, decimal_places=2)
    tipo_embarcacion = models.CharField(max_length=60, choices=TIPOS_EMBARCACION)
    anio = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)])
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class FotoPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='archivos-estaticos/fotos_publicaciones/')
    """
    El upload es necesario porque sino las fotos se almacenan directamente en la base de datos como datos binarios,
    lo que puede hacerla más pesada y menos eficiente para recuperar y manejar
    """