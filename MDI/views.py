from django.shortcuts import render

def home(request):
    
    usuario_actual = request.user
    
    context = {
        'usuario': usuario_actual,
        # no se qué pasar
    }

    return render(request, 'home.html', context)


def terminos_condiciones(request):
    return render(request, 'InformacionMDI/terminos_condiciones.html')


def preguntas_frecuentes(request):
    return render(request, 'InformacionMDI/preguntas_frecuentes.html')

def politicas_privacidad (request):
    return render(request, 'InformacionMDI/politicas_privacidad.html')