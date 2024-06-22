from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views

urlpatterns = [
    path('registrar_usuario/', register_views.registro, name='registrar_usuario'),
    path('perfilDeUsuario/', profile_views.perfil_view, name='perfil_de_usuario' ),
    path('perfilDeUsuario/editar/', profile_views.editar_perfil_view, name='editar_perfil_usuario'),
    path('perfilDeUsuario/actualizar_contraseña/', profile_views.ActualizarPassFormView.as_view(), name='actualizar_contraseña'),
]

