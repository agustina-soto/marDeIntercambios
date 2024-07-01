from django.shortcuts import get_object_or_404, render, redirect
from Aplicaciones.Modelos.models import Room, Usuario
from django.contrib import messages
from utils.Notificacion import NotificationManager

def ver_lista_mensajes(request):
    user = request.user
    _rooms = user.roomsUser.all()
    rooms_with_unread_messages = Room.objects.filter(roomuser__user=user, roomuser__unread_messages=True)
    active_rooms = [room for room in _rooms if room.estado == 'activa']
    context = {
        'active_rooms': active_rooms,
        'rooms_with_unread_messages': rooms_with_unread_messages,
    }  
    return render(request, "ComunicacionEntreUsuarios/Bandeja.html", context)

def eliminar_chat(request):
    if (request.method == 'POST'):
        room_id = request.POST.get('room_id')
        room = get_object_or_404(Room, id=room_id)
        room.estado = 'eliminada'
        room.save()
        notificar_al_otro_usuario(request, room)
        messages.success(request, 'Se eliminó la sala de chat')
    return redirect('bandeja')

def notificar_al_otro_usuario(request, room):
    otro_usuario = room.roomuser_set.exclude(user=request.user)
    mensaje = f'La sala de chat con el usuario {request.user} ha sido eliminada'
    NotificationManager.crear_notificacion(request,  otro_usuario[0].user_id, mensaje, 'sucess')