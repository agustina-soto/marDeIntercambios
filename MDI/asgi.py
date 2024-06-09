import os
import Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Configuro la variable de entorno DJANGO_SETTINGS_MODULE para apuntar al archivo de configuración del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MDI.settings')

# Define la aplicación ASGI para manejar diferentes tipos de conexiones (HTTP y WebSocket)
application = ProtocolTypeRouter({
    # Maneja conexiones HTTP utilizando la aplicación ASGI de Django estándar
    "http": get_asgi_application(),

    # Maneja conexiones WebSocket
    "websocket": AuthMiddlewareStack(
        # URLRouter se usa para enrutar las conexiones WebSocket a las vistas apropiadas basadas en la URL
        URLRouter(
            Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat.routing.websocket_urlpatterns  # Importa las rutas WebSocket desde roomApp.routing
        )
    ),
})
