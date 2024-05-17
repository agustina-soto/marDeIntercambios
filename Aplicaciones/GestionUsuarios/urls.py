from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views

urlpatterns = [
    path('registrar_usuario/', register_views.registro, name='registrar_usuario'),
    path('exitoRegistro/', register_views.exito_registro, name='exito_registro'),

    path('<int:publicacion_id>/editar/', profile_views.render, name='editar_publicacion'), # PENDIENTE
]

