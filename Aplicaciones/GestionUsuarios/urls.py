from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views
from .VerListaUsuarios import views as lista_views
from .BanearUsuario import views as banear_views
from .ActualizarContraseña import views as password_update
from .RecuperarContraseña import views as password_recovery
from .DarDeBajaCuenta import views as desactive_account

urlpatterns = [
    path('registrar_usuario/', register_views.registro, name='registrar_usuario'),
    path('recuperar_password', password_recovery.recuperar_contraseña, name='recuperar_password'),
    path('perfil_de_usuario/<int:user_id>/', profile_views.perfil_view, name='perfil_de_usuario' ),
    path('perfil_de_usuario/<int:user_id>/editar/', profile_views.editar_perfil_view, name='editar_perfil_usuario'),
    path('perfil_de_usuario/<int:user_id>/editar/actualizar_password/', password_update.actualizar_password, name='actualizar_password'),
    path('perfil_de_usuario/<int:user_id>/dar_de_baja_cuenta/', desactive_account.dar_de_baja, name='dar_de_baja_cuenta'),
    path('ver_lista_usuarios/', lista_views.ver_lista_usuarios, name='ver_lista_usuarios'),
    path('ver_lista_usuarios_baneados/', lista_views.ver_lista_usuarios_baneados, name='ver_lista_usuarios_baneados'),
    path('registrar_usuario_administrador/', register_views.registrar_usuario_administrador, name='registrar_usuario_administrador'),
    path('ver_todas_mis_publicaciones/', profile_views.ver_todas_mis_publicaciones, name='ver_todas_mis_publicaciones'),
    path('ver_todas_mis_ofertas/', profile_views.ver_todas_mis_ofertas, name='ver_todas_mis_ofertas'),
    path('banear_usuario/<int:usuario_id>/', banear_views.banear_usuario, name='banear_usuario'),
    path('desbanear_usuario/<int:usuario_id>/', banear_views.desbanear_usuario, name='desbanear_usuario'),
]

