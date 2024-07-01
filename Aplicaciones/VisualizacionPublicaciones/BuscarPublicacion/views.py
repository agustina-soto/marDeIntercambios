from django.shortcuts import render
from django.core.paginator import Paginator
import json

from Aplicaciones.Modelos.models import Publicacion

# Create your views here.
def buscar_publicaciones(request):
    # json_data = open('archivos-estaticos/json/publicaciones.json', encoding='utf-8')   
    # dataPublicaciones = json.load(json_data) # deserialises it
    #dataPublicaciones = Publicacion.objects.all()
    # Comente lo de arriba y agregue la linea de abajo para que no muestre las publicaciones borradas
    dataPublicaciones = Publicacion.objects.exclude(estado='eliminada')

    if request.GET.get('buscar'): ## Si se accede vía POST, se realiza la búsqueda de resultados con la query

        query = request.GET.get('buscar') # Método para retirar valores del QueryDict en POST
        resultados = []
        for element in dataPublicaciones:
            if (query.lower() in element.titulo.lower()):
                resultados.append(element)
                # if (len(resultados) == 10):
                #     break
        
        resultados_paginados = Paginator(resultados, 10)

        if (request.GET.get("page")):
            page_number = request.GET.get("page")
            page_obj = resultados_paginados.get_page(page_number)
        else:
            page_obj = resultados_paginados.get_page(1)

        return render(request, 'VisualizacionPublicaciones/buscar_publicaciones.html', { 'publicaciones': page_obj, 'busqueda': query})
      
    else: ## Si viene por GET, se muestra todo
        resultados = []
        for element in dataPublicaciones:
            resultados.append(element)

        resultados_paginados = Paginator(resultados, 10)
        if (request.GET.get("page")):
            page_number = request.GET.get("page")
            page_obj = resultados_paginados.get_page(page_number)
        else:
            page_obj = resultados_paginados.get_page(1)

        return render(request, 'VisualizacionPublicaciones/buscar_publicaciones.html', { 'publicaciones': page_obj})
