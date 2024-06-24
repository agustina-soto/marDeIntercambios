from Aplicaciones.Modelos.models import Publicacion, Oferta, Room
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from MDI.decorator import login_required
from django.utils.crypto import get_random_string
from Aplicaciones.ComunicacionEntreUsuarios.Correo.views import *
from django.utils import timezone
from utils.Notificacion import NotificationManager

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
        slug = f"{room_name}-{get_random_string(length=6)}"
        room = Room.objects.create(name=room_name, slug=slug)
        room.users.add(publicacion.autor, oferta.autor)
        room.save()