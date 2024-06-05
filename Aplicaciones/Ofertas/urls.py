from django.urls import path
from .views import ver_ofertas
from .views import ver_detalle_oferta
from .views import aceptar_oferta_vista
from .views import rechazar_oferta_vista
from .views import cancelar_oferta_aceptada_vista
from Aplicaciones.Modelos.models import Publicacion

urlpatterns = [
    path('publicacion/<int:publicacion_id>/ofertas/', ver_ofertas, name='ver_ofertas'),
    path('oferta/<int:id>/', ver_detalle_oferta, name='ver_detalle_oferta'),
    path('oferta/<int:oferta_id>/aceptar/', aceptar_oferta_vista, name='aceptar_oferta'),
    path('oferta/<int:oferta_id>/rechazar/', rechazar_oferta_vista, name='rechazar_oferta'),
    path('publicacion/<int:publicacion_id>/cancelar-oferta-aceptada/', cancelar_oferta_aceptada_vista, name='cancelar_oferta_aceptada'),
    
]
