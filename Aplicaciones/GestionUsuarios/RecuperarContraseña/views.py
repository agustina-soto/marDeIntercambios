from django.contrib import messages
from django.shortcuts import render
from Aplicaciones.Modelos.models import Usuario
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

def recuperar_contraseña(request):
    if (request.method == 'POST'):
        correo = request.POST.get('correo')
        if (Usuario.objects.all().filter(username=correo).exists()):
            usuario = Usuario.objects.get(username=correo)
            newPassword = get_random_string(length=8)
            usuario.set_password(newPassword)
            usuario.save()
            enviar_correo(correo, newPassword)
            messages.success(request, "Se envió un mail a su correo electronico")
        else:
            messages.error(request, "El mail ingresado no está registrado en el sistema.")
    return render(request, "GestionUsuarios/recuperar_contraseña.html")

def enviar_correo(correo, password):

    subject = 'Se te ha proporcionado una contraseña'
    from_email = 'somos.glam.tech@gmail.com'
    to = correo
    
    text_content = f'''
    Hola {correo},

    Se te ha generado una contraseña para que puedas ingresar a la plataforma.

    Tu nueva contraseña es: {password}

    Para cambiar la contraseña debes iniciar sesión, ir a tu perfil y dar click en "Actualizar contraseña".

    Saludos,
    GlamTech
    '''
    send_mail(subject, text_content, from_email, [to], fail_silently=False,)