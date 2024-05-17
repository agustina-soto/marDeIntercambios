from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('autenticacion/', include('Aplicaciones.Autenticacion.urls')), #Incluye las URLs de Autenticacion    
    path('publicacion/', include('Aplicaciones.AdministracionPublicaciones.urls')), #Incluye las URLs de AdministrarPublicaciones
    path('usuarios/', include('Aplicaciones.GestionUsuarios.urls')), #Incluye las URLs de GestionUsuario
]