from datetime import timedelta
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from Aplicaciones.Modelos.models import Publicacion, Intercambios

from django.http import HttpResponse


# Create your views here.
def ver_intercambios_activos(request):

    dataPublicaciones = Publicacion.objects.filter(oferta_aceptada_id__isnull=False);

    resultados_paginados = Paginator(dataPublicaciones, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/ver_intercambios_activos.html', { "publicaciones": page_obj});

def finalizar_intercambio (request, publicacion_id):

    pub_instance = Publicacion.objects.get(id=publicacion_id)

    interc_instance = Intercambios.objects.filter(publicacion=publicacion_id)

    
    if(not interc_instance):
        Intercambios.objects.create(publicacion=pub_instance)
    else:
        intercambio = interc_instance[0]
        if (intercambio.estado == "aceptado"):
            messages.error(request, 'El intercambio ya está aceptado')
            return redirect("/intercambios/ver_intercambios_activos")

        intercambio.estado = "aceptado"
        intercambio.fecha_aceptacion = timezone.now()
        intercambio.save()
       
    messages.success(request, 'El intercambio fue aceptado correctametente!')
    return redirect("/intercambios/ver_intercambios_activos")
    

# El método anula la finalización del intercambio siempre y cuando, no hayan pasado más de 3 días de la fecha de aceptación inicial
def anular_finalizacion_intercambio (request, publicacion_id):

    intercambio_instance = Intercambios.objects.filter(publicacion_id=publicacion_id)
    
    if(not intercambio_instance):
        messages.error(request, 'Intercambio inexistente')
        return redirect("/intercambios/ver_intercambios_activos")
    else:
        intercambio = intercambio_instance[0]
        if (intercambio.estado != "aceptado"):
            messages.error(request, 'El intercambio ya está en pendiente')
            return redirect("/intercambios/ver_intercambios_activos")

    # Aquí se verifica que se cumpla la validación, dias no debe ser mayor a 3 para poder anular la finalización.
        ahora = timezone.now()
        fecha_aceptacion = intercambio.fecha_aceptacion
        tiempo_restante = (ahora - fecha_aceptacion)
        dias = tiempo_restante.days

        if (dias > 3):
            messages.error(request, 'No podemos anular el intercambio pues ya pasaron más de 72hs')
        else:
            intercambio.estado = "pendiente";
            intercambio.fecha_aceptacion = None;
            intercambio.save()
            messages.success(request, 'El intercambio fue anulado correctametente!')
        return redirect("/intercambios/ver_intercambios_activos")