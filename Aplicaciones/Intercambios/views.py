from django.shortcuts import render

# Create your views here.
def ver_historial_intercambios(request):

    return render(request, 'Intercambios/ver_historial_intercambios.html')