from django.contrib import admin
from django.urls import path, include
from Aplicaciones.Autenticacion.IniciarSesion import views as iniciarSesion_views
from Aplicaciones.Autenticacion.CerrarSesion import views as cerrarSesion_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('usuarios/login/', iniciarSesion_views.login_view, name='login'),
    path('logout/', cerrarSesion_views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('Aplicaciones.AdministracionPublicaciones.urls')), #Incluye las URLs de la carpeta
]