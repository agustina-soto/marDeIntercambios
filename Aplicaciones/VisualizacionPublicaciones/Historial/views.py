from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from Aplicaciones.Modelos.models import Publicacion, Historial

class HistorialListView(LoginRequiredMixin, ListView):
    model = Historial
    template_name = 'VisualizacionPublicaciones/ver_historial_publicaciones.html'
    context_object_name = 'historial_publicaciones'
    ordering = ['-fecha_visita'] # Ordendo por fecha de visita :)

    def get_queryset(self):
        # Filtra el queryset para obtener solo el historial del usuario actual
        return Historial.objects.filter(usuario=self.request.user)

@login_required
def quitar_de_historial(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    usuario = request.user
    
    # Busca el objeto Historial que relaciona específicamente al usuario con la publicación
    historial_publicacion = Historial.objects.filter(usuario=usuario, publicacion=publicacion).first()

    if historial_publicacion:
        # Elimina el objeto Historial encontrado
        historial_publicacion.delete()
        messages.success(request, 'Publicación removida del historial.')
    else:
        messages.error(request, 'No se encontró historial para esta publicación.')

    # Redirige de vuelta al historial de publicaciones
    return redirect('VisualizacionPublicaciones:ver_historial')