from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Aplicaciones.Modelos.models import Room, Message, RoomUser
from django.http import HttpResponse

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)

    # Control de usuarios
    if not room.users.filter(id=request.user.id).exists():
        return HttpResponse("No tienes permiso para acceder a este sitio")
    
    # Marcar los mensajes como leídos
    RoomUser.objects.filter(user=request.user, room=room).update(unread_messages=False)
    
    if request.method == 'POST':

        content = request.POST.get('content', '')
        foto = request.FILES.get('foto', None)
        
        # Crear el mensaje solo si hay contenido o una foto adjunta
        if content or foto:
            message = Message.objects.create(room=room, user=request.user, content=content, foto=foto)
            message.save()  # Guardar el mensaje para que la foto se almacene correctamente

            # Marcar el mensaje como no leído para todos los usuarios en la sala excepto el que lo envió
            RoomUser.objects.filter(room=room).exclude(user=request.user).update(unread_messages=True)
            
        return redirect(request.path)  # Redirigir al usuario a la misma página después de procesar el formulario

    messages = Message.objects.filter(room=room).order_by('date_added')
    return render(request, 'ComunicacionEntreUsuarios/room.html', {'room': room, 'messages': messages})
