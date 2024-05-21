from django.urls import path, include
from Aplicaciones.VisualizacionPublicaciones.VerDetallePublicacion import views as vistas_visualizacion

urlpatterns = [
    path('ver_detalle/<int:pk>/', vistas_visualizacion.ver_detalle.as_view(), name='ver_detalle')
]

