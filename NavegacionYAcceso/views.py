from django.shortcuts import render

def preguntas_frecuentes(request):
    return render(request, 'NavegacionYAcceso/preguntas_frecuentes.html')

def contacto_puerto_aventura(request):
    return render(request, 'NavegacionYAcceso/contacto_puerto_aventura.html')

def politicas_privacidad(request):
    return render(request, 'NavegacionYAcceso/politicas_privacidad.html')

def terminos_y_condiciones(request):
    return render(request, 'NavegacionYAcceso/terminos_y_condiciones.html')

def informacion_puerto_aventura(request):
    return render(request, 'NavegacionYAcceso/informacion_puerto_aventura.html')

def contacto_equipo_desarrollo(request):
    return render(request, 'NavegacionYAcceso/contacto_equipo_desarrollo.html')