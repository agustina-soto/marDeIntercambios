from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required #Luck: creé el decorator en MDI para reutilizarlo
from django.contrib.auth.decorators import user_passes_test
from MDI.decorator import user_passes_test_superuser #Gio: creé el decorator en MDI para reutilizarlo

from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion, Estado

@login_required 
@user_passes_test_superuser
def ver_publicaciones_para_validar(request):
    dataPublicaciones = Publicacion.objects.filter(estado_id=1);
    # Renderiza la plantilla con los formularios
    return render(request, 'AdministracionPublicaciones/ver_publicaciones_para_validar.html', {"publicaciones" : dataPublicaciones})

def validar_publicacion(request , publicacion_id):

    idEstadoAceptada = Estado.objects.get(nombre="Aceptada")

    infoPublicacion = Publicacion.objects.get(id=publicacion_id);

    infoPublicacion.estado_id = idEstadoAceptada;

    infoPublicacion.save();

    return redirect("/publicacion/ver_publicaciones_para_validar/");

def rechazar_publicacion(request):
    
    return redirect("/publicacion/ver_publicaciones_para_validar/");