from django.urls import path, include
from Aplicaciones.VisualizacionPublicaciones.VerDetallePublicacion import views as vistas_visualizacion
from Aplicaciones.VisualizacionPublicaciones.BuscarPublicacion import views as vistas_buscar_publicaciones
from Aplicaciones.VisualizacionPublicaciones.Favoritos.views import ver_favoritos, agregar_a_favoritos, quitar_de_favoritos

app_name = 'VisualizacionPublicaciones' #crea un namespace para que pueda ser referenciado facielmente en otras aplicaciones

urlpatterns = [
    path('ver_detalle/<int:pk>/', vistas_visualizacion.ver_detalle.as_view(), name='ver_detalle'),
    path('buscar_publicaciones/', vistas_buscar_publicaciones.buscar_publicaciones, name='buscar_publicaciones'),
    path('favoritos/', ver_favoritos, name='ver_favoritos'),
    path('favoritos/agregar/<int:publicacion_id>/', agregar_a_favoritos, name='agregar_a_favoritos'),
    path('favoritos/quitar/<int:publicacion_id>/', quitar_de_favoritos, name='quitar_de_favoritos'),
]