from django.shortcuts import render, redirect

from .forms import EditarPublicacionForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion

def editar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(pk=publicacion_id)
    if request.method == 'POST':
        form = EditarPublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('ruta_hacia_la_vista_de_publicaciones')  # Reemplaza 'ruta_hacia_la_vista_de_publicaciones' con la URL de la vista donde quieres redirigir después de editar la publicación
    else:
        form = EditarPublicacionForm(instance=publicacion)
    return render(request, 'editar_publicacion.html', {'form': form})