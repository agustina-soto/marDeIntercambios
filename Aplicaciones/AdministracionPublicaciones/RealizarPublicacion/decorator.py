from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.') # ME IMPRIME EL MENSAJE REPETIDO, REVISAR POR QUE :(
            return redirect('nombre_de_tu_página_de_inicio_de_sesión') # NO ME VUELVE A LA PAGINA DE INICIO, REVISAR POR QUE :(
        return view_func(request, *args, **kwargs)
    return wrapper
