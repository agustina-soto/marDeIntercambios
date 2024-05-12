from django.db import models

class Usuario(models.Model):
    nombre = models.charField(max_length = 30)
    
# Create your models here.
