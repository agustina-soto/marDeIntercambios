from django.db import models

class Publicacion(models.Model):
    titulo=models.CharField(max_length=50)
    precio_minimo_permitido=models.FloatField()
    tipo_embarcación=models.CharField(max_length=50)
    anio=models.DateField()
    #lo de la foto no se como agregarlo a la clase todavia, tengo que hacer el template