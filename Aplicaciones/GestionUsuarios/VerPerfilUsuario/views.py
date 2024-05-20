from django.shortcuts import render

# Creando los modelos de ver
def perfil_view(request):
    return render(request, 'perfilDeUsuario.html')