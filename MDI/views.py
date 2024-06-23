from django.shortcuts import render
from Aplicaciones.Modelos.models import Publicacion
from django.core.paginator import Paginator


def home(request):
    # Obtiiene todas las publicaciones excluyendo las eliminadas
    dataPublicaciones = Publicacion.objects.exclude(estado='eliminada')

    # Paginan los resultados
    resultados_paginados = Paginator(dataPublicaciones, 10)
    page_number = request.GET.get("page")
    page_obj = resultados_paginados.get_page(page_number if page_number else 1)

    return render(request, 'home.html', {'publicaciones': page_obj})