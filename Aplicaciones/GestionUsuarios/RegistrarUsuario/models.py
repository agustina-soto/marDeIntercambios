from django.db import models

class Usuario(models.Model):
    nombre = models.charField(max_length = 100)
    
# Create your models here.
