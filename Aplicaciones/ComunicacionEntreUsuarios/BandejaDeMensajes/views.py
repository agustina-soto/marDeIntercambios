from django.shortcuts import render
from Aplicaciones.Modelos.models import Room

def ver_lista_mensajes(request):
    user = request.user
    _rooms = user.rooms.all()
    return render(request, "ComunicacionEntreUsuarios/Bandeja.html", {'rooms': _rooms})