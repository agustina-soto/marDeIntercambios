from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from MDI.decorator import login_required
from Aplicaciones.Modelos.models import Publicacion, Oferta
from MDI.decorator import login_required

@login_required
def borrar_publicacion(request, publicacion_id):
    if request.method == 'GET':
        if publicacion_id:
            publicacion = get_object_or_404(Publicacion, id=publicacion_id)
            publicacion.estado = 'eliminada'
            publicacion.save()

            # Rechaza todas las ofertas asociadas a esta publicación
            ofertas = Oferta.objects.filter(publicacion=publicacion)
            for oferta in ofertas:
                oferta.estado = 'rechazada'
                oferta.save()

            messages.success(request, '¡La publicación ha sido eliminada correctamente!')
            return redirect('ver_detalle', pk=publicacion_id)
    messages.error(request, '¡Ha ocurrido un error al intentar eliminar la publicación!')
    return redirect('inicio')
