from django.shortcuts import render

from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion, FotoPublicacion #importo el modelo de otra app
from django.views.generic.detail import DetailView

class ver_detalle (DetailView):
    model = Publicacion
    template_name = 'ver_detalle.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el objeto Publicacion actual
        publicacion = self.get_object()
        # Agrega las fotos relacionadas al contexto
        context['fotos'] = FotoPublicacion.objects.filter(publicacion=publicacion)
        return context