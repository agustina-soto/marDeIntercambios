from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.detail import DetailView
from .models import Oferta, FotoOferta
from .forms import OfertaForm, FotoOfertaForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from django.contrib.auth.decorators import login_required

@login_required  #es para asegurar que solo los usuarios autenticados pueden tener acceso a esta vista
def realizar_oferta(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id) #obtiene un objeto de la base de datos en caso de que no se encuentre, genera un error 404 (página no encontrada).

    if request.method == 'POST':
        oferta_form = OfertaForm(request.POST, publicacion=publicacion)  # Pasamos la publicacion aquí
        foto_form = FotoOfertaForm(request.POST, request.FILES)

        if oferta_form.is_valid():
            oferta = oferta_form.save(commit=False) #permite quedarte con una instancia del modelo de oferta antes de que se guarde en la base de datos
            oferta.autor = request.user #asocio quien realiza la oferta con la oferta
            oferta.publicacion = publicacion #asocio la publicacion con la oferta 
            oferta.save()

            if foto_form.is_valid():
                fotos = request.FILES.getlist('foto')
                # Crea una instancia de FotoOferta para cada foto cargada, enlazándola con la oferta
                for foto in fotos:
                    FotoOferta.objects.create(oferta=oferta, foto=foto)# Establece la relación entre Oferta y FotoOferta

            # Muestra un mensaje de éxito y redireccionar a algún lugar apropiado
            messages.success(request, '¡La oferta se realizó con éxito!')
            return redirect('ver_detalle_oferta', pk=oferta.pk)
        else:
            # Muestra un mensaje de error si los formularios no son válidos
            messages.error(request, '¡No se pudo realizar la oferta!')
    else:
        # Si la solicitud no es POST, crea instancias de formularios vacíos
        oferta_form = OfertaForm(publicacion=publicacion)
        foto_form = FotoOfertaForm()

    # Renderiza la plantilla con los formularios
    return render(request, 'AdminitracionIntercambio/realizar_oferta.html', {'oferta_form': oferta_form, 'foto_form': foto_form})

class ver_detalle_oferta (DetailView):
    model = Oferta
    template_name = 'AdminitracionIntercambio/ver_detalle_oferta.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el objeto Oferta actual
        oferta = self.get_object()
        # Agrega las fotos relacionadas al contexto
        context['fotos'] = FotoOferta.objects.filter(oferta=oferta)
        # Verifica si el usuario actual es el dueño de la oferta
        context['es_dueno'] = self.request.user == oferta.autor
        return context

        
