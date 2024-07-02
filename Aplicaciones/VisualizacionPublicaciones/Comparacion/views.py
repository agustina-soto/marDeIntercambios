from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Aplicaciones.Modelos.models import Publicacion

def seleccionar_publicacion(request, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        publicaciones_seleccionadas = request.session.get('publicaciones_a_comparar', [])

        if publicacion_id not in publicaciones_seleccionadas:
            if len(publicaciones_seleccionadas) < 3:
                publicaciones_seleccionadas.append(publicacion_id)
                messages.success(request, f'Se ha seleccionado la publicación "{publicacion.titulo}" para comparar.')
            else:
                messages.warning(request, 'Ya has seleccionado el máximo de 3 publicaciones para comparar.')
        request.session['publicaciones_a_comparar'] = publicaciones_seleccionadas

    return redirect('VisualizacionPublicaciones:ver_publicaciones')


def deseleccionar_publicacion(request, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        publicaciones_seleccionadas = request.session.get('publicaciones_a_comparar', [])

        if publicacion_id in publicaciones_seleccionadas:
            publicaciones_seleccionadas.remove(publicacion_id)
            messages.success(request, f'Se ha deseleccionado la publicación "{publicacion.titulo}".')
        request.session['publicaciones_a_comparar'] = publicaciones_seleccionadas

    return redirect('VisualizacionPublicaciones:ver_publicaciones')


def comparar_publicaciones(request):
    publicaciones_seleccionadas = request.session.get('publicaciones_a_comparar', [])

    if len(publicaciones_seleccionadas) < 2:
        messages.warning(request, 'Debes seleccionar al menos 2 publicaciones para comparar.')
        return redirect('home')

    # Publicaciones seleccionadas
    publicaciones = Publicacion.objects.filter(id__in=publicaciones_seleccionadas)

    context = {
        'publicaciones': publicaciones,
    }

    return render(request, 'VisualizacionPublicaciones/comparar_publicaciones.html', context)
