from django.urls import path
from .RealizarPublicacion import views as submit_views
from .EditarPublicacion import views as edit_views
from .BorrarPublicacion import views as delete_views

urlpatterns = [
    path('realizar_publicacion/', submit_views.realizar_publicacion, name='realizar_publicacion'),
    path('editar/<int:publicacion_id>/', edit_views.editar_publicacion, name='editar_publicacion'),
    # Para editar una publicacion, el link es 'dominio/publicacion/editar/idPublicacion'
    #path('eliminar_foto/', edit_views.eliminar_foto, name='eliminar_foto'),
    path('borrar/<int:publicacion_id>/', delete_views.borrar_publicacion, name='borrar_publicacion'),
]
