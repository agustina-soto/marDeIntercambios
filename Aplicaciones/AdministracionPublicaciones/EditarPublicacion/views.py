from django.shortcuts import render, redirect

from .forms import EditarPublicacionForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion

def editar_publicacion(request, publicacion_id):
    publicacion = Publicacion.objects.get(pk=publicacion_id)
    if request.method == 'POST':
        form = EditarPublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('ver_detalle.html') #Este tiene que ser el html de maite, recordar usar el mismo nombre!
    else:
        form = EditarPublicacionForm(instance=publicacion)
    return render(request, 'editar_publicacion.html', {'form': form})