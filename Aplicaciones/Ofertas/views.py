from Aplicaciones.Modelos.models import Publicacion, Oferta, FotoOferta, Room, Usuario
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from MDI.decorator import login_required
from django.utils.crypto import get_random_string
from Aplicaciones.ComunicacionEntreUsuarios.Correo.views import *
from django.utils import timezone
from utils.Notificacion import NotificationManager
from django.contrib import messages
from django.urls import reverse
from .forms import OfertaForm, FotoOfertaForm, EditarOfertaForm

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
                return redirect('ver_detalle_oferta', id=oferta.id)
        else:
            # Muestra un mensaje de error si los formularios no son válidos
            messages.error(request, '¡No se pudo realizar la oferta!')
    else:
        # Si la solicitud no es POST, crea instancias de formularios vacíos
        oferta_form = OfertaForm(publicacion=publicacion)
        foto_form = FotoOfertaForm()


    # Renderiza la plantilla con los formularios
    return render(request, 'Ofertas/realizar_oferta.html', {'oferta_form': oferta_form, 'foto_form': foto_form})

@login_required
def eliminar_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, id=oferta_id)

    if oferta.estado == 'aceptada' or oferta.estado == 'Aceptada':
        messages.error(request, "No se puede eliminar la ofetra porque ya fue aceptada")
        return redirect(reverse('VisualizacionPublicaciones:ver_detalle', kwargs={'pk': oferta.publicacion.pk}))#"reverse" genera URLs a partir de nombres de vistas y parámetros para redireccionar a una vista especifica
    
    #si la oferta no fue aceptada se puede eliminar y se cambia el estado de la oferta a eliminada 
    oferta.estado = 'eliminada'
    oferta.save()

    messages.success(request, "La oferta ha sido eliminada exitosamente.")
    return redirect(reverse('VisualizacionPublicaciones:ver_detalle', kwargs={'pk': oferta.publicacion.pk}))

def crear_autor(oferta_form, _pass):
    unUser = oferta_form.cleaned_data['visitante']
    unDni = oferta_form.cleaned_data['dni']
    unaFechaNacimiento = oferta_form.cleaned_data['fecha_nacimiento']
    nuevoUsuario = Usuario.objects.create(username=unUser, dni=unDni,fecha_nacimiento=unaFechaNacimiento)
    nuevoUsuario.set_password(_pass)
    nuevoUsuario.save()
    return nuevoUsuario

@login_required
def ver_ofertas(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    try:
        ofertas = publicacion.ofertas_publicacion.all()
    except Publicacion.DoesNotExist:
        ofertas = None
    return render(request, 'Ofertas/ver_ofertas.html', {'publicacion': publicacion, 'ofertas': ofertas})

@login_required
def ver_detalle_oferta(request, id):
    try:
        oferta = Oferta.objects.get(id=id)
    except Oferta.DoesNotExist:
        raise Http404("La oferta no existe")
    return render(request, 'Ofertas/ver_detalle_oferta.html', {'oferta': oferta})
    
@login_required
def aceptar_oferta_vista(request, oferta_id):
    if request.method == 'POST':
        oferta = get_object_or_404(Oferta, id=oferta_id)
        try:
            publicacion = oferta.publicacion
            publicacion.aceptar_oferta(oferta)
            #Se crea notificacion
            gestorNotis = NotificationManager()
            gestorNotis.crear_notificacion(user=oferta.autor.id, message="Su oferta por la publicación: " + oferta.publicacion.titulo + " ha sido ACEPTADA", tipo="success")

            #enviar_correo(request, oferta, 'correo/oferta_aceptada.html')
            #Se crea sala si no existe
            crear_sala(publicacion, oferta)
            return redirect('ver_ofertas', publicacion_id=publicacion.id)
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse("Esta vista solo acepta solicitudes POST.")

@login_required
def rechazar_oferta_vista(request, oferta_id):
    if request.method == 'POST':
        oferta = get_object_or_404(Oferta, id=oferta_id)
        try:
            publicacion = oferta.publicacion
            publicacion.rechazar_oferta(oferta)
            # SE CREA NOTIFICACION
            gestorNotis = NotificationManager()
            gestorNotis.crear_notificacion(user=oferta.autor.id, message="Su oferta por la publicación: " + oferta.publicacion.titulo + " ha sido RECHAZADA", tipo="error")
            
            #enviar_correo(request, oferta, 'correo/oferta_rechazada.html')
            return redirect('ver_ofertas', publicacion_id=publicacion.id)
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse("Esta vista solo acepta solicitudes POST.")

@login_required
def cancelar_oferta_aceptada_vista(request, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        if publicacion.oferta_aceptada:
            oferta_aceptada = publicacion.oferta_aceptada
            try:
                publicacion.cancelar_oferta_aceptada()
                #SE CREA NOTIFICACION
                gestorNotis = NotificationManager()
                gestorNotis.crear_notificacion(user=oferta_aceptada.autor.id, message="Su oferta por la publicación: " + oferta_aceptada.publicacion.titulo + " ha sido CANCELADA", tipo="warning")

                #enviar_correo(request, oferta_aceptada, 'correo/oferta_cancelada.html')
                return redirect('ver_ofertas', publicacion_id=publicacion_id)
            except Exception as e:
                return HttpResponse(str(e))
        else:
            return HttpResponse("No hay oferta aceptada para cancelar.")
    else:
        return HttpResponse("Esta vista solo acepta solicitudes POST.")
    
#agregar que solo puedan acceder user logeados
def editar_oferta (request, oferta_id):
    # Obtenemos la instancia de la oferta que queremos editar a partir del ID proporcionado
    oferta = get_object_or_404(Oferta, pk=oferta_id) #Oferta.objects.get(pk=oferta_id)
    # Obtenemos la publicación asociada a la oferta
    publicacion = oferta.publicacion 
    # Obtenemos todas las fotos asociadas a esta oferta
    fotos_oferta = FotoOferta.objects.filter(oferta=oferta)

    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos enviados y la publicación existente
        oferta_form = EditarOfertaForm(request.POST, instance=oferta, publicacion=publicacion)
        # Obtenemos las nuevas fotos que se han subido
        fotos_nuevas = request.FILES.getlist('foto')
        # Obtenemos la lista de IDs de las fotos que se han marcado para eliminar
        fotos_a_eliminar_ids = [id for id in request.POST.get('fotos_a_eliminar', '').split(',') if id]

        if oferta_form.is_valid():
            # Guardar la oferta con los nuevos datos
            oferta_form.save()
            
            # Eliminar las fotos marcadas para eliminación
            for foto_id in fotos_a_eliminar_ids:
                try:
                    foto_a_eliminar = FotoOferta.objects.get(pk=foto_id)
                    foto_a_eliminar.delete()
                except FotoOferta.DoesNotExist:
                    pass

            # Agregar las nuevas fotos subidas
            for foto in fotos_nuevas:
                FotoOferta.objects.create(oferta=oferta, foto=foto)

            messages.success(request, '¡Se editó la oferta!')
            return redirect('ver_detalle_oferta', id=oferta.id)
        else:
            # Si el formulario no es válido, mostramos un mensaje de error
            messages.error(request, '¡No se pudo editar la oferta!')
    
    else:
        # Si la solicitud no es POST, creamos una instancia del formulario con los datos actuales de la publicación
        oferta_form = EditarOfertaForm(instance=oferta, publicacion=publicacion)

    # Renderizamos la plantilla 'editar_oferta.html' con el formulario y las fotos de la oferta
    return render(request, 'Ofertas/editar_oferta.html', {
        'oferta_form': oferta_form,
        'fotos_oferta': fotos_oferta,
    })





"""    
def enviar_correo(request, oferta, _template):
    if request.method == 'POST':
        destinatario = oferta.autor.username
        asunto = 'Publicación: ' + oferta.publicacion.titulo
        nombre = oferta.autor.username  # nombre al que le mando el correo
        template = _template  # plantilla a usar
        enviar_email_oferta(destinatario, asunto, nombre, template, oferta)


def enviar_correo(request, oferta, _template):
    if (request.method == 'POST'):
        destinatario = oferta.autor.username
        asunto = 'Publicación: ' + oferta.publicacion.titulo
        nombre = oferta.autor.username #nombre al que le mando el correo
        template = _template #plantilla a usar
        enviar_email_oferta(destinatario, asunto, nombre, template, oferta)
    return render(request, 'correo/correo.html')
"""

def crear_sala(publicacion, oferta):
    existe_room = Room.objects.filter(users__in=[publicacion.autor, oferta.autor], name=f"Sala-{publicacion.titulo}").first()
    if not existe_room:
        room_name = f"Sala-{publicacion.titulo}"
        slug = f"{publicacion.autor.id}-{oferta.autor.id}{get_random_string(length=8)}"
        room = Room.objects.create(name=room_name, slug=slug)
        room.users.add(publicacion.autor, oferta.autor)
        room.save()
    