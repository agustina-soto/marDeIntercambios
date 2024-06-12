from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def enviar_email_oferta(destinatario, asunto, nombre, template, oferta):
    from_email = settings.DEFAULT_FROM_EMAIL
    
    # Contenido del mensaje en texto plano
    text_content = 'Este es el contenido del correo en texto plano.'
    
    # Generar contenido HTML a partir de una plantilla
    html_content = render_to_string(template, {'nombre': nombre, 'oferta': oferta })

    msg = EmailMultiAlternatives(asunto, text_content, from_email, [destinatario])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

"""
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.conf import settings

def enviar_email_oferta(destinatario, asunto, nombre, template, oferta):
    from_email = settings.EMAIL_HOST_USER
    
    # Contenido del mensaje en texto plano
    text_content = 'Este es el contenido del correo en texto plano.'
    
    # Generar contenido HTML a partir de una plantilla
    html_content = render_to_string(template, {'nombre': nombre, 'oferta': oferta })

    msg = EmailMultiAlternatives(asunto, text_content, from_email, [destinatario])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def enviar_email_oferta_realizada(destinatario, asunto, nombre, template, oferta, password):
    from_email = settings.EMAIL_HOST_USER
    
    # Contenido del mensaje en texto plano
    text_content = 'Este es el contenido del correo en texto plano.'
    
    # Generar contenido HTML a partir de una plantilla
    html_content = render_to_string(template, {'nombre': nombre, 'oferta': oferta, 'contraseña': password})

    msg = EmailMultiAlternatives(asunto, text_content, from_email, [destinatario])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
"""