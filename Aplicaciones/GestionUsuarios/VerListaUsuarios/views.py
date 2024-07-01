from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render
from django.contrib import messages
from Aplicaciones.Modelos.models import Usuario
from MDI.decorator import login_required, user_passes_test_superuser
from django.contrib.auth.decorators import login_required # por que hay 2 login required importados??
from django.core.paginator import Paginator

@login_required 
@user_passes_test_superuser
def ver_lista_usuarios(request):
    dataUsuarios = Usuario.objects.all();

    resultados_paginados = Paginator(dataUsuarios, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)

    # Renderiza la plantilla con los formularios
    return render(request, 'GestionUsuarios/ver_lista_usuarios.html', {"usuarios" : page_obj})

def ver_lista_usuarios_baneados(request):
    dataUsuarios = Usuario.objects.filter(bloqueado=1);

    resultados_paginados = Paginator(dataUsuarios, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)

    # Renderiza la plantilla con los formularios
    return render(request, 'GestionUsuarios/ver_lista_usuarios_baneados.html', {"usuarios" : page_obj})

