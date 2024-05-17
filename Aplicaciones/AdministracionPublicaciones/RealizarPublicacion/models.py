from django.db import models
from .choices import TIPOS_EMBARCACION

class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    precio_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_embarcacion = models.CharField(max_length=50, choices=TIPOS_EMBARCACION)
    anio = models.IntegerField()
    foto = models.ImageField(upload_to='publicaciones_fotos/', default='static/images/default.png')
