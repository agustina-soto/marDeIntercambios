from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views

urlpatterns = [
    path('registrar_usuario/', register_views.registro, name='registrar_usuario'),
    path('perfilDeUsuario/', profile_views.perfil_view, name='perfil_de_usuario' )
]

