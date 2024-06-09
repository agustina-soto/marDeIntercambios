from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.shortcuts import render, get_object_or_404
from .models import Room, Message


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room).order_by('date_added')
    return render(request, 'ComunicacionEntreUsuarios/room.html', {'room': room, 'messages': messages})