from django.urls import path
from .RealizarPublicacion import views as submit_views
from .EditarPublicacion import views as edit_views
from .ValidarPublicaciones import views as validate_views
from .BorrarPublicacion import views as delete_views

urlpatterns = [
    path('realizar_publicacion/', submit_views.realizar_publicacion, name='realizar_publicacion'),
    path('editar/<int:publicacion_id>/', edit_views.editar_publicacion, name='editar_publicacion'),
    path('ver_publicaciones_para_validar/', validate_views.ver_publicaciones_para_validar, name='ver_publicaciones_para_validar'),
    path('validar_publicacion/<int:publicacion_id>/', validate_views.validar_publicacion, name='validar_publicacion'),
    path('rechazar_publicacion/<int:publicacion_id>/<str:justificacion>/', validate_views.rechazar_publicacion, name='rechazar_publicacion'),
    # Para editar una publicacion, el link es 'dominio/publicacion/editar/idPublicacion'
    #path('eliminar_foto/', edit_views.eliminar_foto, name='eliminar_foto'),
    path('borrar/<int:publicacion_id>/', delete_views.borrar_publicacion, name='borrar_publicacion'),
]
