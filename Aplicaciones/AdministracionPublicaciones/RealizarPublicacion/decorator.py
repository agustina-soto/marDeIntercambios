from django.shortcuts import redirect
from django.contrib import messages
from Aplicaciones.Autenticacion.urls import iniciarSesion_views

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
