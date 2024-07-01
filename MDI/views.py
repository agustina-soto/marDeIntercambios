from django.shortcuts import render
from Aplicaciones.Modelos.models import Publicacion
from django.core.paginator import Paginator

def home(request):
    # Obtiene todas las publicaciones excluyendo las eliminadas
    dataPublicaciones = Publicacion.objects.exclude(estado='eliminada')

    # Pagina los resultados
    resultados_paginados = Paginator(dataPublicaciones, 10)
    page_number = request.GET.get("page")
    page_obj = resultados_paginados.get_page(page_number if page_number else 1)

    # Obtiene las publicaciones seleccionadas de la sesión
    publicaciones_seleccionadas = request.session.get('publicaciones_a_comparar', [])

    # Pasa las publicaciones y las publicaciones seleccionadas al contexto
    context = {
        'publicaciones': page_obj,
        'publicaciones_a_comparar': publicaciones_seleccionadas,
    }

    return render(request, 'home.html', context)


def terminos_condiciones(request):
    return render(request, 'InformacionMDI/terminos_condiciones.html')


def preguntas_frecuentes(request):
    return render(request, 'InformacionMDI/preguntas_frecuentes.html')

def politicas_privacidad (request):
    return render(request, 'InformacionMDI/politicas_privacidad.html')