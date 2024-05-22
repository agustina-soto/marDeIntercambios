from django.shortcuts import render
from django.core.paginator import Paginator
import json
from django.http import HttpResponse

from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion

# Create your views here.
def buscar_publicaciones(request):
    # json_data = open('archivos-estaticos/json/publicaciones.json', encoding='utf-8')   
    # dataPublicaciones = json.load(json_data) # deserialises it
    dataPublicaciones = Publicacion.objects.all()
    
    if request.GET.get('buscar'): ## Si se accede vía POST, se realiza la búsqueda de resultados con la query

        query = request.GET.get('buscar') # Método para retirar valores del QueryDict en POST
        resultados = []
        for element in dataPublicaciones:
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
            page_obj = resultados_paginados.get_page(1)

        return render(request, 'buscar_publicaciones.html', { 'publicaciones': page_obj, 'busqueda': query})
      
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

        return render(request, 'buscar_publicaciones.html', { 'publicaciones': page_obj})

# def carga_manual (request):
    publi = Publicacion(id=1, titulo="Velero de telgopor I", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=2, titulo="Velero de telgopor II", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=3, titulo="Velero de cemento III", tipo_embarcacion="velero", precio_minimo=12000, anio=2010) 
    publi.save()
    publi = Publicacion(id=4, titulo="Velero de telgopor IV", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=5, titulo="Velero de telgopor V", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=6, titulo="Velero de telgopor VI", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=7, titulo="Velero de telgopor VII", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=8, titulo="Velero de telgopor VIII", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=9, titulo="Velero de telgopor IX", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=10, titulo="Velero de telgopor X", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()
    publi = Publicacion(id=11, titulo="Velero de telgopor XI", tipo_embarcacion="velero", precio_minimo=20000, anio=1997) 
    publi.save()


    return HttpResponse("return this string")
