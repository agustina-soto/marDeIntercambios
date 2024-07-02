from django.urls import path
from .views import ver_ofertas
from .views import ver_detalle_oferta
from .views import aceptar_oferta_vista
from .views import rechazar_oferta_vista
from .views import cancelar_oferta_aceptada_vista
from .views import realizar_oferta
from .views import editar_oferta
from .views import eliminar_oferta
from Aplicaciones.Modelos.models import Publicacion

urlpatterns = [
    path('ver-ofertas/<int:publicacion_id>/', ver_ofertas, name='ver_ofertas'),
    path('ver-detalle-oferta/<int:id>/', ver_detalle_oferta, name='ver_detalle_oferta'),
    path('aceptar-oferta/<int:oferta_id>/', aceptar_oferta_vista, name='aceptar_oferta'),
    path('rechazar-oferta/<int:oferta_id>/', rechazar_oferta_vista, name='rechazar_oferta'),
    path('cancelar-oferta-aceptada/<int:publicacion_id>/', cancelar_oferta_aceptada_vista, name='cancelar_oferta_aceptada'),
    path('realizar_oferta/<int:publicacion_id>/', realizar_oferta, name='realizar_oferta'),
    path('editar_oferta/<int:oferta_id>/', editar_oferta, name='editar_oferta'),
    path('eliminar_oferta/<int:oferta_id>/', eliminar_oferta, name='eliminar_oferta'),
    # falta la vista para que un usuario pueda ver sus propias ofertas
]
