from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def user_passes_test_superuser(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, 'No tenes acceso a la pantalla seleccionada.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper