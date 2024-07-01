from django.urls import path

from .views import ver_intercambios_activos;
from .views import historial_intercambios;
from .views import finalizar_intercambio;
from .views import anular_finalizacion_intercambio;
from .views import calificar_intercambio_propietario
from .views import calificar_intercambio_comprador


urlpatterns = [
    path('ver_intercambios_activos/', ver_intercambios_activos, name='ver_intercambios_activos'),
    path('historial_intercambios/', historial_intercambios, name='historial_intercambios'),
    path('finalizar_intercambio/<int:publicacion_id>/', finalizar_intercambio, name='finalizar_intercambio'),
    path('anular_finalizacion_intercambio/<int:publicacion_id>/', anular_finalizacion_intercambio, name='anular_finalizacion_intercambio'),
    path('calificar/<int:intercambio_id>/prop/<int:autor_id>/', calificar_intercambio_propietario, name='calificar_intercambio_propietario'),
    path('calificar/<int:intercambio_id>/compr/<int:comprador_id>/', calificar_intercambio_comprador, name='calificar_intercambio_comprador'),
]
