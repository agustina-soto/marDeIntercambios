from datetime import timedelta
from django.db.models.functions import ExtractDay
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from Aplicaciones.Modelos.models import Publicacion, Intercambios
from utils.Notificacion import NotificationManager

from django.http import HttpResponse


# Create your views here.
def ver_intercambios_activos(request):
    
    dataPublicaciones = Publicacion.objects.filter(oferta_aceptada_id__isnull=False);
    arrayDatos = [];
    for pub in dataPublicaciones:
        dias = 0;
        int = Intercambios.objects.filter(publicacion=pub.id);
        # print("Pub: " + str(pub.id))
        # int = Intercambios.objects.filter(publicacion=pub.id, estado='aceptado').exists()
        if (int):
            int = int[0];
            # print("Intercambio: " + str(int.id) + " - Estado: " + int.estado)
            estado = int.estado;

            if (int.fecha_aceptacion):
                ## Chequeo de tiempo
                ahora = timezone.now()
                fecha_aceptacion = int.fecha_aceptacion
                tiempo_restante = (ahora - fecha_aceptacion)
                dias = tiempo_restante.days

        else:
            # print("No hay Intercambio aún " + " - Estado: pendiente por default")
            estado = "pendiente";
            
        
        if ((estado == "pendiente") or (estado == "aceptado" and (dias < 3 ))):

            diccionario = {
                "estado_intercambio": estado,
                "detalle": pub
            }

            arrayDatos.append(diccionario);


    print(arrayDatos);
    # resultados_paginados = Paginator(dataPublicaciones, 10)
    resultados_paginados = Paginator(arrayDatos, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/ver_intercambios_activos.html', { "publicaciones": page_obj});

def historial_intercambios(request):

    dataIntercambios = Intercambios.objects.filter(estado="aceptado");

    for dataI in dataIntercambios:
        print(dataI.publicacion.autor.dni);

    resultados_paginados = Paginator(dataIntercambios, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/historial_intercambios.html', { "intercambios": page_obj});

def finalizar_intercambio (request, publicacion_id):

    pub_instance = Publicacion.objects.get(id=publicacion_id)

    interc_instance = Intercambios.objects.filter(publicacion=publicacion_id)

    
    if(not interc_instance):
        intercambio = Intercambios.objects.create(publicacion=pub_instance)
    else:
        intercambio = interc_instance[0]
        if (intercambio.estado == "aceptado"):
            messages.error(request, 'El intercambio ya fue finalizado con anterioridad')
            return redirect("/intercambios/ver_intercambios_activos")

        intercambio.estado = "aceptado"
        intercambio.fecha_aceptacion = timezone.now()
        intercambio.save()
    
    gestorNotis = NotificationManager()
    gestorNotis.crear_notificacion(user=pub_instance.autor.id, message="El intercambio" + str(intercambio.id) + " ha sido marcado como FINALIZADO", tipo="success")
    messages.success(request, 'El intercambio fue finalizado correctamente!')
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
            messages.success(request, 'El intercambio fue anulado correctamente!')
            gestorNotis = NotificationManager()
            gestorNotis.crear_notificacion(user=intercambio.publicacion.autor.id, message="El intercambio " + str(intercambio.id) + " ha sido marcado ANULADO", tipo="error")
        return redirect("/intercambios/ver_intercambios_activos")