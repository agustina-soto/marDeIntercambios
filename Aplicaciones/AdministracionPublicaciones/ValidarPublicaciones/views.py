from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required #Luck: creé el decorator en MDI para reutilizarlo
from django.contrib.auth.decorators import user_passes_test
from MDI.decorator import user_passes_test_superuser #Gio: creé el decorator en MDI para reutilizarlo
from Aplicaciones.Modelos.models import Publicacion, Notificacion

@login_required 
@user_passes_test_superuser
def ver_publicaciones_para_validar(request):
    dataPublicaciones = Publicacion.objects.filter(estado="pendiente");

    resultados_paginados = Paginator(dataPublicaciones, 10)

    if (request.GET.get("page")):
        page_number = request.GET.get("page")
        page_obj = resultados_paginados.get_page(page_number)
    else:
        page_obj = resultados_paginados.get_page(1)

    # Renderiza la plantilla con los formularios
    return render(request, 'AdministracionPublicaciones/ver_publicaciones_para_validar.html', {"publicaciones" : page_obj})

def validar_publicacion(request , publicacion_id):

    infoPublicacion = Publicacion.objects.get(id=publicacion_id);

    infoPublicacion.estado = "aceptada";

    infoPublicacion.save();

    ## NOTIFICAR AL USUARIO
    Notificacion.objects.create(fecha=timezone.now(), user=infoPublicacion.autor, descripcion="La publicación " + str(infoPublicacion.id) + " ha sido ACEPTADA")

    messages.success(request, 'Publicación aceptada correctamente')
    return redirect("/publicacion/ver_publicaciones_para_validar/");

def rechazar_publicacion(request, publicacion_id, justificacion):
    infoPublicacion = Publicacion.objects.get(id=publicacion_id);
    
    ## FALTA NOTIFICAR AL USUARIO
    Notificacion.objects.create(fecha=timezone.now(), user=infoPublicacion.autor, descripcion="La publicación fue rechazada por el siguiente motivo: " + justificacion)
    messages.success(request, 'Publicación cancelada correctamente')
    return redirect("/publicacion/ver_publicaciones_para_validar/");