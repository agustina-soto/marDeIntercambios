from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views
from .ActualizarContraseña import views as password_update
from .RecuperarContraseña import views as password_recovery
from .DarDeBajaCuenta import views as desactive_account

urlpatterns = [
    path('registrarUsuario/', register_views.registro, name='registrar_usuario'),
    path('recuperarPassword', password_recovery.recuperar_contraseña, name='recuperar_password'),
    path('perfilDeUsuario/', profile_views.perfil_view, name='perfil_de_usuario' ),
    path('perfilDeUsuario/editar/', profile_views.editar_perfil_view, name='editar_perfil_usuario'),
    path('perfilDeUsuario/actualizarPassword/', password_update.actualizar_password, name='actualizar_password'),
    path('perfilDeUsuario/darDeBajaCuenta/', desactive_account.dar_de_baja, name='dar_de_baja_cuenta'),
]

