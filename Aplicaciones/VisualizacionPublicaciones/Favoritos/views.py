from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Aplicaciones.Modelos.models import Publicacion

@login_required
def ver_favoritos(request):
    usuario = request.user
    publicaciones_favoritas = usuario.favoritos.all()
    return render(request, 'VisualizacionPublicaciones/ver_favoritos.html', {'publicaciones_favoritas': publicaciones_favoritas})


@login_required
def agregar_a_favoritos(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    usuario = request.user

    if publicacion in usuario.favoritos.all(): # esto no deberia estar porque no deberia mostrarse el boton si ya esta en sus fav, pero podemos dejarlo por si falla algo
        messages.info(request, 'La publicación ya está en tus favoritos.')
    else:
        usuario.favoritos.add(publicacion)
        messages.success(request, 'Publicación agregada a favoritos.')

    return redirect('VisualizacionPublicaciones:ver_detalle', pk=publicacion.id) # Agrega a favoritos y redirige al detalle de la publicacion

@login_required
def quitar_de_favoritos(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    usuario = request.user
    publicaciones_favoritas = usuario.favoritos.all()
    if publicacion in usuario.favoritos.all():
        usuario.favoritos.remove(publicacion)
        messages.success(request, 'Publicación removida de favoritos.')
    else:
        messages.success(request, 'No puedes quitar esta publicación porque no está en tus favoritos.')

    return render(request, 'VisualizacionPublicaciones/ver_favoritos.html', {'publicaciones_favoritas': publicaciones_favoritas}) # Quita de favoritos y redirige al detalle de la publicacion