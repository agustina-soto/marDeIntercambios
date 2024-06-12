from django.db import models
from Aplicaciones.GestionUsuarios.RegistrarUsuario.models import Usuario
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from Aplicaciones.Modelos.models import Oferta, FotoOferta

"""
class Oferta (models.Model):
    precio_estimado = models.DecimalField(max_digits=7, decimal_places=2)
    descripcion = models.TextField(max_length=260)
    estado = models.CharField(max_length=10, default="pendiente") #no se si deberia de ser un string 
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='publicacion')
    autor = models.ForeignKey(
        Usuario,                   # Modelo al que está relacionado
        on_delete=models.CASCADE,  # Comportamiento de eliminación en cascada
        related_name='ofertas'     # Nombre para acceder a las ofertas desde Usuario
    )

class FotoOferta (models.Model):
    oferta = models.ForeignKey(Oferta, related_name='fotos', on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='archivos-estaticos/fotos_ofertas/', null=True, blank=True)#permino que tenga valor nulo o vacio en este campo

"""
