import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, RegistroFormAdministrador
from .models import *
from MDI.decorator import login_required, user_passes_test_superuser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) #Se verifcan datos dentro del form y se genera instancia de un usuario para su registro
        if form.is_valid(): #si no ocurrió ningún error...
            try:
                form.save()
                #usuario = form.save() 
                #login(request, usuario) #No sé si hace falta loguear al usuario que se registre, la h.u no lo especifica
                messages.success(request, "Usuario Registrado con éxito!")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = RegistroForm()
    return render(request, 'GestionUsuarios/registro.html', {'form': form})


@login_required 
@user_passes_test_superuser
def registrar_usuario_administrador(request):
    if request.method == 'POST':
        form = RegistroFormAdministrador(request.POST)
        if form.is_valid():
            try:
                usuario = form.save(commit=False)
                
                # Generar una contraseña aleatoria
                contraseña_aleatoria = generar_contraseña_aleatoria()
                print(contraseña_aleatoria)
                usuario.password = make_password(contraseña_aleatoria)
                usuario.is_superuser = True
                usuario.save()

                enviar_correo_usuario_admin(usuario.username, contraseña_aleatoria)

                messages.success(request, "Usuario Administrador Registrado con éxito!")
            except Exception as e:
                form.add_error(None, str(e))
        else:
            print(form.errors)
            messages.error(request, "Error en el formulario. Por favor, revisa los campos.")
    else:
        form = RegistroFormAdministrador()
    
    return render(request, 'GestionUsuarios/registro_administrador.html', {'form': form})

def generar_contraseña_aleatoria(length=8):
    # Genera una contraseña aleatoria de la longitud especificada
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for i in range(length))

def enviar_correo_usuario_admin(correo, password):

    subject = 'Se te ha proporcionado una contraseña'
    from_email = 'somos.glam.tech@gmail.com'
    to = correo
    
    text_content = f'''
    Hola {correo},

    Se te ha generado un usuario administrador para que puedas ingresar a la plataforma.

    Tu nueva contraseña es: {password}

    Para cambiar la contraseña debes iniciar sesión, ir a tu perfil y dar click en "Actualizar contraseña".

    Saludos,
    GlamTech
    '''
    send_mail(subject, text_content, from_email, [to], fail_silently=False,)