from django.shortcuts import render
from Aplicaciones.Modelos.models import Room

def ver_lista_mensajes(request):
    user = request.user
    rooms_with_unread_messages = Room.objects.filter(roomuser__user=user, roomuser__unread_messages=True)
    print(rooms_with_unread_messages)
    _rooms = user.roomsUser.all()
    return render(request, "ComunicacionEntreUsuarios/Bandeja.html", {'rooms': _rooms, 'rooms_with_unread_messages': rooms_with_unread_messages})