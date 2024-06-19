from django.urls import path
from Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat.views import room
from Aplicaciones.ComunicacionEntreUsuarios.BandejaDeMensajes.views import ver_lista_mensajes

urlpatterns = [
    path("<slug:slug>/", room, name='room'),
    path("", ver_lista_mensajes, name='bandeja'),
]