from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import logout # Encargada de cerrar la sesion
from django.shortcuts import redirect # Recibe un string (la dir a donde deseamos redirigir)

def logout_view(request):
    logout(request) #La peticion ya conoce la sesion
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')