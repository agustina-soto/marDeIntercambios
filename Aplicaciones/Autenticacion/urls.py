from django.urls import path
from Aplicaciones.Autenticacion.IniciarSesion import views as iniciarSesion_views
from .CerrarSesion  import views as cerrarSesion_views

urlpatterns = [
    path('login/', iniciarSesion_views.login_view, name='login'),
    path('logout/', cerrarSesion_views.logout_view, name='logout'),
]

