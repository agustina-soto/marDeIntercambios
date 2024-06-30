from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from MDI.decorator import login_required
from Aplicaciones.Modelos.models import Intercambios, Publicacion, Oferta
from MDI.decorator import login_required

@login_required
def borrar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'GET':
        # Verifica si hay intercambios aceptados asociados a la publicación, si los hay no te deja borrar
        intercambios_aceptados = Intercambios.objects.filter(publicacion=publicacion, estado='aceptado').exists()

        if intercambios_aceptados:
            messages.error(request, 'No puedes eliminar esta publicación porque tiene intercambios aceptados.')
            return redirect('VisualizacionPublicaciones:ver_detalle', pk=publicacion.pk)

        # Si no hay intercambios aceptados, proceder con la eliminación de la publicación
        publicacion.estado = 'eliminada'
        publicacion.save()

        # Rechaza todas las ofertas asociadas a esta publicación
        Oferta.objects.filter(publicacion=publicacion).update(estado='rechazada')

        # Rechaza el intercambio asociado a la publicación (si lo hubiese)
        try:
            intercambio = Intercambios.objects.get(publicacion=publicacion)
            intercambio.estado = 'rechazado'
            intercambio.save()
        except Intercambios.DoesNotExist:
            pass

        messages.success(request, '¡La publicación ha sido eliminada correctamente!')
        return redirect('VisualizacionPublicaciones:ver_detalle', pk=publicacion.pk)

    messages.error(request, '¡Ha ocurrido un error al intentar eliminar la publicación!')
    return redirect('home') # tenia 'inicio' acá, no encontré nada definido así pero recuerdo haberlo declarado asique si falla es por esto