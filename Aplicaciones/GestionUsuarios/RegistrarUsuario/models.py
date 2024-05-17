from django.db import models

class UsuarioRegistrado(models.Model):
    email = models.EmailField(primary_key=True)
    contraseña = models.CharField(max_length=100)
    dni = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return self.email