from django.urls import path

from .views import ver_intercambios_activos;
from .views import finalizar_intercambio;
from .views import anular_finalizacion_intercambio;

urlpatterns = [
    path('ver_intercambios_activos/', ver_intercambios_activos, name='ver_intercambios_activos'),
    path('finalizar_intercambio/<int:publicacion_id>/', finalizar_intercambio, name='finalizar_intercambio'),
    path('anular_finalizacion_intercambio/<int:publicacion_id>/', anular_finalizacion_intercambio, name='anular_finalizacion_intercambio'),
]
