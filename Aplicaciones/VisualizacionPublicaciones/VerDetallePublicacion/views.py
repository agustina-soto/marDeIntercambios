from django.shortcuts import render
from django.views.generic.detail import DetailView
from Aplicaciones.Modelos.models import Publicacion, FotoPublicacion, Historial

class ver_detalle (DetailView):
    model = Publicacion
    template_name = 'VisualizacionPublicaciones/ver_detalle.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs): # Tuve que redefinir el metodo get del DetailView
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            publicacion = self.get_object()
            # Registra la publicacion en el historial del usuario
            Historial.objects.create(usuario=request.user, publicacion=publicacion)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el objeto Publicacion actual
        publicacion = self.get_object()
        # Agrega las fotos relacionadas al contexto
        context['fotos'] = FotoPublicacion.objects.filter(publicacion=publicacion)
        # Verifica si el usuario actual es el dueño de la publicación
        context['es_dueno'] = self.request.user == publicacion.autor
        return context