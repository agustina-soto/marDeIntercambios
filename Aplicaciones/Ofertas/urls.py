from django.urls import path
from .views import ver_ofertas
from .views import ver_detalle_oferta
from .views import aceptar_oferta_vista
from .views import rechazar_oferta_vista
from .views import cancelar_oferta_aceptada_vista
from Aplicaciones.Modelos.models import Publicacion

urlpatterns = [
    path('ver-ofertas/<int:publicacion_id>/', ver_ofertas, name='ver_ofertas'),
    path('ver-detalle-oferta/<int:id>/', ver_detalle_oferta, name='ver_detalle_oferta'),
    path('aceptar-oferta/<int:oferta_id>/', aceptar_oferta_vista, name='aceptar_oferta'),
    path('rechazar-oferta/<int:oferta_id>/', rechazar_oferta_vista, name='rechazar_oferta'),
    path('cancelar-oferta-aceptada/<int:publicacion_id>/', cancelar_oferta_aceptada_vista, name='cancelar_oferta_aceptada'),
    
]
