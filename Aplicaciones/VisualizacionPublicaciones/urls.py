from django.urls import path, include
from Aplicaciones.VisualizacionPublicaciones.VerDetallePublicacion import views as vistas_visualizacion
from Aplicaciones.VisualizacionPublicaciones.BuscarPublicacion import views as vistas_buscar_publicaciones

urlpatterns = [
    path('ver_detalle/<int:pk>/', vistas_visualizacion.ver_detalle.as_view(), name='ver_detalle'),
    path('buscar_publicaciones/', vistas_buscar_publicaciones.buscar_publicaciones, name='buscar_publicaciones')
]

