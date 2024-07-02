"""from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from Aplicaciones.Modelos.models import Oferta, FotoOferta, Usuario
from MDI.decorator import login_required #Agrego usuario
from .forms import OfertaForm, FotoOfertaForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from django.utils.crypto import get_random_string #Agregado
from Aplicaciones.ComunicacionEntreUsuarios.Correo.views import * #Agregado(PARA EL EMAIL)
from django.utils import timezone
from utils.Notificacion import NotificationManager

@login_required
def realizar_oferta(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id) #obtiene un objeto de la base de datos en caso de que no se encuentre, genera un error 404 (página no encontrada).

    if request.method == 'POST':
        oferta_form = OfertaForm(request.POST, request=request, publicacion=publicacion)  # Pasamos la publicacion aquí, request para verificar usuario autenticado
        foto_form = FotoOfertaForm(request.POST, request.FILES)

        if oferta_form.is_valid():
            oferta = oferta_form.save(commit=False) #permite quedarte con una instancia del modelo de oferta antes de que se guarde en la base de datos
            
            #Agrego logica de creación de usuario en caso de que sea visitante
            unPassword = get_random_string(length=10)
            if not request.user.is_authenticated:
                unAutor = crear_autor(oferta_form, unPassword)
            else:
                unAutor = request.user

            oferta.autor = unAutor#asocio quien realiza la oferta con la oferta (USAMOS ACÁ)
            oferta.publicacion = publicacion #asocio la publicacion con la oferta 
            oferta.save()
            
            if foto_form.is_valid():
                fotos = request.FILES.getlist('foto')
                # Crea una instancia de FotoOferta para cada foto cargada, enlazándola con la oferta
                for foto in fotos:
                    FotoOferta.objects.create(oferta=oferta, foto=foto)# Establece la relación entre Oferta y FotoOferta
            
            
            # Muestra un mensaje de éxito y redireccionar a algún lugar apropiado
            messages.success(request, '¡La oferta se realizó con éxito!')
             #Se crea notificacion
            gestorNotis = NotificationManager()
            gestorNotis.crear_notificacion(user=oferta.publicacion.autor.id, message="Se ha recibido una oferta por la publicacion: " + oferta.publicacion.titulo, tipo="success")

            if not request.user.is_authenticated:
                #enviar_correo(request, oferta, 'correo/oferta_creada_visitante.html', unPassword)
                pass
            else:
                #enviar_correo(request, oferta, 'correo/oferta_creada_visitante.html', '')
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
    
@login_required
def eliminar_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)

    if oferta.estado == 'aceptada':
        messages.error(request, "No se puede eliminar la ofetra porque ya fue aceptada")
        return redirect(reverse('VisualizacionPublicaciones:ver_detalle', kwargs={'pk': oferta.publicacion.id}))#"reverse" genera URLs a partir de nombres de vistas y parámetros para redireccionar a una vista especifica
    
    #si la oferta no fue aceptada se puede eliminar y se cambia el estado de la oferta a eliminada 
    oferta.estado = 'eliminada'
    oferta.save()

    messages.success(request, "La oferta ha sido eliminada exitosamente.")
    return redirect(reverse('VisualizacionPublicaciones:ver_detalle', kwargs={'pk': oferta.publicacion.id}))

def crear_autor(oferta_form, _pass):
    unUser = oferta_form.cleaned_data['visitante']
    unDni = oferta_form.cleaned_data['dni']
    unaFechaNacimiento = oferta_form.cleaned_data['fecha_nacimiento']
    nuevoUsuario = Usuario.objects.create(username=unUser, dni=unDni,fecha_nacimiento=unaFechaNacimiento)
    nuevoUsuario.set_password(_pass)
    nuevoUsuario.save()
    return nuevoUsuario

"""
"""def  enviar_correo(request, oferta, _template, _pass):
    if (request.method == 'POST'):
        destinatario = oferta.autor.username
        asunto = 'Oferta creada'
        nombre = oferta.autor.username #nombre al que le mando el correo
        template = _template #plantilla a usar
        enviar_email_oferta_realizada(destinatario, asunto, nombre, template, oferta, _pass)
"""