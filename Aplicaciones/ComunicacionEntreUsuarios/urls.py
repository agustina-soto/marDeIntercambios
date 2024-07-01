from django.urls import path
from Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat.views import room
from Aplicaciones.ComunicacionEntreUsuarios.BandejaDeMensajes.views import ver_lista_mensajes, eliminar_chat

urlpatterns = [
    path("", ver_lista_mensajes, name='bandeja'),
    path("eliminar_chat/", eliminar_chat, name='eliminar_chat'),
    path("<slug:slug>/", room, name='room'),
]