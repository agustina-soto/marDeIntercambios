from . import views
from MDI import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('usuarios/', include('Aplicaciones.GestionUsuarios.urls')), #Incluye las URLs de GestionUsuario
    path('autenticacion/', include('Aplicaciones.Autenticacion.urls')), #Incluye las URLs de Autenticacion    
    path('publicacion/', include('Aplicaciones.AdministracionPublicaciones.urls')), #Incluye las URLs de AdministrarPublicaciones
    path('publicacion/ver-publicacion/', include('Aplicaciones.VisualizacionPublicaciones.urls')), #Incluye las URLs de VisualizacionPublicaciones
    path('ofertas/', include('Aplicaciones.Ofertas.urls')), #Incluye las URLs de Ofertas
    path('intercambios/', include('Aplicaciones.Intercambios.urls')), #Incluye las URLs de Intercambios
    path('chats/', include('Aplicaciones.ComunicacionEntreUsuarios.urls')),
    path('notificaciones/', include('Aplicaciones.Notificaciones.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)