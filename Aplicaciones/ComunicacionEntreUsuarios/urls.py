from django.urls import path
from Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat.views import room

urlpatterns = [
    path('<slug:slug>/', room, name='room'),
]