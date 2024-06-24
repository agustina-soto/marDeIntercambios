from django.shortcuts import render, redirect
from Aplicaciones.Modelos.models import Notificacion
from utils.Notificacion import NotificationManager

def lista_notificaciones(request):
    gestorNotis = NotificationManager()
    notis = gestorNotis.get_notificaciones(user=request.user)
    return render(request, 'Notificaciones/notificaciones.html', {'notificaciones': notis})