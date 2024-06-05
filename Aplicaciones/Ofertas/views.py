from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from Aplicaciones.Modelos.models import Publicacion, Oferta
from django.core.mail import send_mail
from django.template.loader import render_to_string

def ver_ofertas(request, publicacion_id):
    publicacion = Publicacion.objects.get(id=publicacion_id)
    ofertas = publicacion.ofertas.all()

    if request.method == 'POST':
        oferta_id = request.POST.get('oferta_id')
        oferta = Oferta.objects.get(pk=oferta_id)

        # Si la URL contiene 'aceptar', se acepta la oferta
        if 'aceptar' in request.path:
            try:
                publicacion.aceptar_oferta(oferta)
                return HttpResponse("Oferta aceptada correctamente")
            except Exception as e:
                return HttpResponse(str(e))
            
        # Si la URL contiene 'rechazar', se rechaza la oferta
        elif 'rechazar' in request.path:
            try:
                publicacion.rechazar_oferta(oferta)
                return HttpResponse("Oferta rechazada correctamente")
            except Exception as e:
                return HttpResponse(str(e))
    
    return render(request, 'Ofertas/ver_ofertas.html', {'publicacion': publicacion, 'ofertas': ofertas})


def ver_detalle_oferta(request, id):
    try:
        oferta = Oferta.objects.get(id=id)
    except Oferta.DoesNotExist:
        raise Http404("La oferta no existe")
    return render(request, 'Ofertas/ver_detalle_oferta.html', {'oferta': oferta})

    
def aceptar_oferta_vista(request, oferta_id):
    oferta = Oferta.objects.get(id=oferta_id)
    publicacion = oferta.publicacion
    try:
        publicacion.aceptar_oferta(oferta) # Llama al metodo de la clase Publicacion para aceptar la oferta

        # Envío del correo electrónico al ofertante
        subject = '¡Tu oferta ha sido aceptada!'
        context = {'oferta': oferta}  # Datos a pasar a la plantilla
        html_message = render_to_string('Correo/oferta_aceptada.html', context)
        from_email = 'tu_correo@gmail.com'  # Remitente del correo
        to_email = oferta.autor.email  # Correo electrónico del ofertante
        send_mail(subject, '', from_email, [to_email], html_message=html_message)

        return HttpResponse("Oferta aceptada")
    except Exception as e:
        return HttpResponse(str(e))


def rechazar_oferta_vista(request, oferta_id):
    oferta = Oferta.objects.get(id=oferta_id)
    publicacion = oferta.publicacion
    try:
        publicacion.rechazar_oferta(oferta)

        # Envío del correo electrónico al ofertante
        subject = '¡Tu oferta ha sido rechazada!'
        context = {'oferta': oferta}  # Datos a pasar a la plantilla
        html_message = render_to_string('Correo/oferta_rechazada.html', context)
        from_email = 'tu_correo@gmail.com'  # Remitente del correo
        to_email = oferta.autor.email  # Correo electrónico del ofertante
        send_mail(subject, '', from_email, [to_email], html_message=html_message)

        return HttpResponse("Oferta rechazada")
    except Exception as e:
        return HttpResponse(str(e))


def cancelar_oferta_aceptada_vista(request, publicacion_id):
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
        if publicacion.oferta_aceptada:
            oferta_aceptada = publicacion.oferta_aceptada

            # Cancelar la oferta aceptada
            publicacion.cancelar_oferta_aceptada()

            # Envío del correo electrónico al ofertante
            subject = '¡Tu oferta ha sido cancelada!'
            context = {'oferta': oferta_aceptada}  # Datos a pasar a la plantilla
            html_message = render_to_string('Correo/oferta_cancelada.html', context)
            from_email = 'tu_correo@gmail.com'  # Remitente del correo
            to_email = oferta_aceptada.autor.email  # Correo electrónico del ofertante
            send_mail(subject, '', from_email, [to_email], html_message=html_message)

            return redirect('ver_ofertas', publicacion_id=publicacion_id)
        else:
            return HttpResponse("No hay oferta aceptada para cancelar.")
    except Publicacion.DoesNotExist:
        return HttpResponse("La publicación no existe.")
