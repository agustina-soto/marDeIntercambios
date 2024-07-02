from django.shortcuts import render
from Aplicaciones.Modelos.models import Publicacion
from django.core.paginator import Paginator

def ver_publicaciones(request):
    # Obtiene todas las publicaciones excluyendo las eliminadas
    publicaciones = Publicacion.objects.exclude(estado__in=['eliminada', 'Eliminada'])

    # Pagina los resultados
    resultados_paginados = Paginator(publicaciones, 10)
    page_number = request.GET.get("page")
    page_obj = resultados_paginados.get_page(page_number if page_number else 1)

    # Obtiene las publicaciones seleccionadas de la sesión
    publicaciones_seleccionadas = request.session.get('publicaciones_a_comparar', [])

    # Pasa las publicaciones y las publicaciones seleccionadas al contexto
    context = {
        'publicaciones': page_obj,
        'publicaciones_a_comparar': publicaciones_seleccionadas,
    }
    return render(request, 'VisualizacionPublicaciones/publicaciones.html', context)