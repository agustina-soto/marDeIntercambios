from django.urls import path
from .RealizarPublicacion import views as submit_views
from .EditarPublicacion import views as edit_views

urlpatterns = [
    path('realizar_publicacion/', submit_views.realizar_publicacion, name='realizar_publicacion'),
    path('<int:publicacion_id>/editar/', edit_views.editar_publicacion, name='editar_publicacion'),
]
