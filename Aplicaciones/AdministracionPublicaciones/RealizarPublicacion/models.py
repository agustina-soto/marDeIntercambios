import random
import string
from django.db import models
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Publicacion(models.Model):
    titulo = models.CharField(max_length=50)
    precio_minimo = models.DecimalField(max_digits=7, decimal_places=2)
    tipo_embarcacion = models.CharField(max_length=60, choices=TIPOS_EMBARCACION)
    anio = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)])

class FotoPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='publicaciones_fotos/')

    def default_title(): 
        return 'foto_' + str(FotoPublicacion.id) + '_' + generate_random_str()

    titulo = models.CharField(max_length=50, default=default_title)  

def generate_random_str(length=7): 
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

"""
class FotoPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='publicaciones_fotos/')

    def default_title(self): # Genera un título predeterminado único.
        return 'foto_' + str(self.id) + '_' + generate_random_str()
   
    titulo = models.CharField(max_length=50, default=default_title)  # Título predeterminado único
    

def generate_random_str(length=7): # Genera una cadena aleatoria de caracteres.
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
"""