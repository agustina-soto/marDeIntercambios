from django.urls import path
from .RegistrarUsuario import views as register_views
from .VerPerfilUsuario import views as profile_views
from .VerListaUsuarios import views as lista_views
from .BanearUsuario import views as banear_views

urlpatterns = [
    path('registrar_usuario/', register_views.registro, name='registrar_usuario'),
    path('perfilDeUsuario/', profile_views.perfil_view, name='perfil_de_usuario' ),
    path('perfilDeUsuario/editar/', profile_views.editar_perfil_view, name='editar_perfil_usuario'),
    path('ver_lista_usuarios/', lista_views.ver_lista_usuarios, name='ver_lista_usuarios'),
    path('ver_lista_usuarios_baneados/', lista_views.ver_lista_usuarios_baneados, name='ver_lista_usuarios_baneados'),
    path('registrar_usuario_administrador/', register_views.registrar_usuario_administrador, name='registrar_usuario_administrador'),
    path('banear_usuario/<int:usuario_id>/', banear_views.banear_usuario, name='banear_usuario'),
]

