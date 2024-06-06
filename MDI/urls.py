from django.urls import path, include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('usuarios/', include('Aplicaciones.GestionUsuarios.urls')), #Incluye las URLs de GestionUsuario
    path('autenticacion/', include('Aplicaciones.Autenticacion.urls')), #Incluye las URLs de Autenticacion    
    path('publicacion/', include('Aplicaciones.AdministracionPublicaciones.urls')), #Incluye las URLs de AdministrarPublicaciones
    path('publicacion/ver-publicacion/', include('Aplicaciones.VisualizacionPublicaciones.urls')), #Incluye las URLs de VisualizacionPublicaciones
    path('oferta/', include('Aplicaciones.AdministracionIntercambio.urls')), #Incluye las URLs de Administracion de Intercambios
]