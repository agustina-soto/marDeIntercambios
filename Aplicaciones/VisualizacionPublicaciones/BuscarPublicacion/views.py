from django.shortcuts import render
from django.core.paginator import Paginator
import json

# Create your views here.
def buscar_publicaciones(request):
    json_data = open('archivos-estaticos/json/publicaciones.json', encoding='utf-8')   
    data1 = json.load(json_data) # deserialises it
    # data2 = json.dumps(data1) # json formatted string
    
    if request.GET.get('buscar'): ## Si se accede vía POST, se realiza la búsqueda de resultados con la query

        query = request.GET.get('buscar') # Método para retirar valores del QueryDict en POST
        resultados = [];
        for element in data1:
            if (query.lower() in element['titulo'].lower()):
                resultados.append(element)
                # if (len(resultados) == 10):
                #     break
        
        print("RESULTADOS FULL " , resultados)
        resultados_paginados = Paginator(resultados, 10)

        if (request.GET.get("page")):
            page_number = request.GET.get("page")
            page_obj = resultados_paginados.get_page(page_number)
        else:
            page_obj = resultados_paginados.get_page(1);

        return render(request, 'buscar_publicaciones.html', { 'publicaciones': page_obj, 'busqueda': query})
      
    else: ## Si viene por GET, se muestra todo
        resultados = [];
        for element in data1:
            resultados.append(element)

        resultados_paginados = Paginator(resultados, 10)
        if (request.GET.get("page")):
            page_number = request.GET.get("page")
            page_obj = resultados_paginados.get_page(page_number)
        else:
            page_obj = resultados_paginados.get_page(1);

        return render(request, 'buscar_publicaciones.html', { 'publicaciones': page_obj})
