from django.shortcuts import render, redirect
from Aplicaciones.Modelos.models import Notificacion

def lista_notificaciones(request):
    notis = Notificacion.objects.filter(user=request.user)
    return render(request, 'Notificaciones/notificaciones.html', {'notificaciones': notis})