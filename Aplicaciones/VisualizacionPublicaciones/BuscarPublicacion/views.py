from django.shortcuts import render
from django.core.paginator import Paginator
import json

from Aplicaciones.Modelos.models import Publicacion

# # Create your views here.
# def buscar_publicaciones(request):
#     # json_data = open('archivos-estaticos/json/publicaciones.json', encoding='utf-8')   
#     # dataPublicaciones = json.load(json_data) # deserialises it
#     #dataPublicaciones = Publicacion.objects.all()
#     # Comente lo de arriba y agregue la linea de abajo para que no muestre las publicaciones borradas
#     dataPublicaciones = Publicacion.objects.exclude(estado='eliminada')

#     if request.GET.get('buscar'): ## Si se accede vía POST, se realiza la búsqueda de resultados con la query

#         query = request.GET.get('buscar') # Método para retirar valores del QueryDict en POST
#         resultados = []
#         for element in dataPublicaciones:
#             if (query.lower() in element.titulo.lower()):
#                 resultados.append(element)
#                 # if (len(resultados) == 10):
#                 #     break
        
#         resultados_paginados = Paginator(resultados, 10)

#         if (request.GET.get("page")):
#             page_number = request.GET.get("page")
#             page_obj = resultados_paginados.get_page(page_number)
#         else:
#             page_obj = resultados_paginados.get_page(1)

#         return render(request, 'VisualizacionPublicaciones/buscar_publicaciones.html', { 'publicaciones': page_obj, 'busqueda': query})
      
#     else: ## Si viene por GET, se muestra todo
#         resultados = []
#         for element in dataPublicaciones:
#             resultados.append(element)

#         resultados_paginados = Paginator(resultados, 10)
#         if (request.GET.get("page")):
#             page_number = request.GET.get("page")
#             page_obj = resultados_paginados.get_page(page_number)
#         else:
#             page_obj = resultados_paginados.get_page(1)

#         return render(request, 'VisualizacionPublicaciones/buscar_publicaciones.html', { 'publicaciones': page_obj})

def buscar_publicaciones(request):
    dataPublicaciones = Publicacion.objects.exclude(estado='eliminada')

    query = request.GET.get('buscar')
    tipo = request.GET.get('tipo')
    valor_min = request.GET.get('valor_min')
    valor_max = request.GET.get('valor_max')
    anio_min = request.GET.get('anio_min')
    anio_max = request.GET.get('anio_max')

    if query:
        dataPublicaciones = dataPublicaciones.filter(titulo__icontains=query)
    if tipo:
        dataPublicaciones = dataPublicaciones.filter(tipo_embarcacion=tipo)
    if valor_min:
        dataPublicaciones = dataPublicaciones.filter(precio_minimo__gte=valor_min)
    if valor_max:
        dataPublicaciones = dataPublicaciones.filter(precio_minimo__lte=valor_max)
    if anio_min:
        dataPublicaciones = dataPublicaciones.filter(anio__gte=anio_min)
    if anio_max:
        dataPublicaciones = dataPublicaciones.filter(anio__lte=anio_max)

    resultados_paginados = Paginator(dataPublicaciones, 10)
    page_number = request.GET.get("page")
    page_obj = resultados_paginados.get_page(page_number)

    tipos_de_embarcacion = Publicacion.objects.values_list('tipo_embarcacion', flat=True).distinct()

    context = {
        'publicaciones': page_obj,
        'busqueda': query,
        'tipos_de_embarcacion': tipos_de_embarcacion,
        'valor_min': valor_min,
        'valor_max': valor_max,
        'anio_min': anio_min,
        'anio_max': anio_max,
    }

    return render(request, 'VisualizacionPublicaciones/buscar_publicaciones.html', context)