from datetime import timedelta
from django.db.models.functions import ExtractDay
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from Aplicaciones.Modelos.models import Publicacion, Intercambios
from utils.Notificacion import NotificationManager
from MDI.decorator import login_required, user_passes_test_superuser

from django.http import HttpResponse


# Create your views here.
@login_required 
@user_passes_test_superuser
def ver_intercambios_activos(request):
    
    ## Los intercambios solo son posibles con publicaciones aceptadas
    # dataPublicaciones = Publicacion.objects.filter(oferta_aceptada_id__isnull=False, estado="aceptada");
    dataPublicaciones = Publicacion.objects.filter(oferta_aceptada_id__isnull=False)
    arrayDatos = []
    for pub in dataPublicaciones:
        dias = 0
        int = Intercambios.objects.filter(publicacion=pub.id)
        # print("Pub: " + str(pub.id))
        int = Intercambios.objects.filter(publicacion=pub.id, estado='aceptado')
        if (int):
            int = int[0]
            # print("Intercambio: " + str(int.id) + " - Estado: " + int.estado)
            estado = int.estado

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


    # resultados_paginados = Paginator(dataPublicaciones, 10)
    resultados_paginados = Paginator(arrayDatos, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/ver_intercambios_activos.html', { "publicaciones": page_obj});

@login_required 
@user_passes_test_superuser
def historial_intercambios(request):

    dataIntercambios = Intercambios.objects.filter(estado="aceptado");

    # for dataI in dataIntercambios:
    #     print(dataI.publicacion.autor.dni);

    resultados_paginados = Paginator(dataIntercambios, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/historial_intercambios.html', { "intercambios": page_obj})

@login_required 
@user_passes_test_superuser
def finalizar_intercambio (request, publicacion_id):

    pub_instance = Publicacion.objects.get(id=publicacion_id)

    pub_instance.estado = "finalizada"
    pub_instance.save()

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

    mensajeNotiAutor = f"El intercambio de la publicación '{pub_instance.titulo}' ha sido marcado como Finalizado, haga <a href='/intercambios/calificar/{intercambio.id}/prop/{pub_instance.autor.id}'>click aquí para calificar su experiencia</a>"
    mensajeNotiCompr = f"El intercambio de la publicación '{pub_instance.titulo}' ha sido marcado como Finalizado, haga <a href='/intercambios/calificar/{intercambio.id}/compr/{pub_instance.oferta_aceptada.autor.id}'>click aquí para calificar su experiencia</a>"
    gestorNotis = NotificationManager()
    gestorNotis.crear_notificacion(user=pub_instance.autor.id, message=mensajeNotiAutor, tipo="success")
    gestorNotis.crear_notificacion(user=pub_instance.oferta_aceptada.autor.id, message=mensajeNotiCompr, tipo="success")
    messages.success(request, 'El intercambio fue finalizado correctamente!')
    return redirect("/intercambios/ver_intercambios_activos")
    

# El método anula la finalización del intercambio siempre y cuando, no hayan pasado más de 3 días de la fecha de aceptación inicial
@login_required 
@user_passes_test_superuser
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
            pub_instance = Publicacion.objects.filter(id=intercambio.publicacion)[0]

            pub_instance.estado = "aceptada"
            pub_instance.save()


            intercambio.estado = "pendiente";
            intercambio.fecha_aceptacion = None;
            intercambio.save()
            messages.success(request, 'El intercambio fue anulado correctamente!')
            gestorNotis = NotificationManager()
            gestorNotis.crear_notificacion(user=intercambio.publicacion.autor.id, message="El intercambio " + str(intercambio.id) + " ha sido marcado ANULADO", tipo="error")
        return redirect("/intercambios/ver_intercambios_activos")

@login_required    
def calificar_intercambio_propietario(request, intercambio_id, autor_id):
    intercambio = Intercambios.objects.filter(id=intercambio_id)[0]
    if request.method == 'POST':
        print('Entramos por POST')

        intercambio.calificacion_autor = request.POST.get('calification-input')

        if request.POST.get('textAreaCalificacion'):
            intercambio.descripcion_autor = request.POST.get('textAreaCalificacion')


        intercambio.save()

        return render(request, 'Intercambios/calificacion_realizada.html')
    else:
        if (intercambio.calificacion_autor):
            messages.warning(request, 'Este intercambio ya fue calificado anteriormente')
            return redirect('home')
        if (intercambio.estado == "rechazado"):
            messages.error(request, '¡No se puede realizar la calificación de un intercambio rechazado!')
            return redirect('home')
        if (intercambio.estado == "pendiente"):
            messages.warning(request, '¡No se puede realizar la calificación de un intercambio no finalizado!')
            return redirect('home')
        
        
        
        context = {
            "range": range(1,11),
            "intercambio": intercambio_id,
            "autor": autor_id
        }

        return render(request, 'Intercambios/calificar_intercambio_propietario.html', { "context" : context })

@login_required   
def calificar_intercambio_comprador(request, intercambio_id, comprador_id):
    intercambio = Intercambios.objects.filter(id=intercambio_id)[0]
    if request.method == 'POST':
        print('Entramos por POST')

        intercambio.calificacion_comprador = request.POST.get('calification-input')

        if request.POST.get('textAreaCalificacion'):
            intercambio.descripcion_comprador = request.POST.get('textAreaCalificacion')
        
        intercambio.save()
        
        return render(request, 'Intercambios/calificacion_realizada.html')
    else:
        if (intercambio.calificacion_comprador):
            messages.warning(request, 'Este intercambio ya fue calificado anteriormente')
            return redirect('home')
        if (intercambio.estado == "rechazado"):
            messages.error(request, '¡No se puede realizar la calificación de un intercambio rechazado!')
            return redirect('home')
        if (intercambio.estado == "pendiente"):
            messages.warning(request, '¡No se puede realizar la calificación de un intercambio no finalizado!')
            return redirect('home')
        
        
        
        context = {
            "range": range(1,11),
            "intercambio": intercambio_id,
            "comprador": comprador_id
        }

        return render(request, 'Intercambios/calificar_intercambio_comprador.html', { "context" : context })

@login_required 
@user_passes_test_superuser   
def ver_calificaciones(request):

    dataIntercambios = Intercambios.objects.filter(estado="aceptado");

    resultados_paginados = Paginator(dataIntercambios, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)


    return render(request, 'Intercambios/lista_calificaciones.html', { "intercambios": page_obj})