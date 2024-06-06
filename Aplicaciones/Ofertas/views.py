from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from Aplicaciones.Modelos.models import Publicacion, Oferta

@login_required
def ver_ofertas(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    try:
        ofertas = publicacion.ofertas.all()
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
            enviarCorreo(oferta, 'aceptada', 'Correo/oferta_aceptada.html')
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
            enviarCorreo(oferta, 'rechazada', 'Correo/oferta_rechazada.html')
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
                enviarCorreo(oferta_aceptada, 'cancelada', 'Correo/oferta_cancelada.html')
                return redirect('ver_ofertas', publicacion_id=publicacion_id)
            except Exception as e:
                return HttpResponse(str(e))
        else:
            return HttpResponse("No hay oferta aceptada para cancelar.")
    else:
        return HttpResponse("Esta vista solo acepta solicitudes POST.")

# No funciona :(
def enviarCorreo(oferta, accion, html):
    subject = f'¡Tu oferta ha sido {accion}!'
    context = {'oferta': oferta}
    html_message = render_to_string(html, context)
    from_email = 'somos.glam.tech@gmail.com'
    to_email = oferta.autor.email
    print('enviando correo')
    send_mail(subject, '', from_email, [to_email], html_message=html_message)