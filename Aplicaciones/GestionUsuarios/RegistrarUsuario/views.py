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

                # try:
                #     send_mail(
                #         'Tu cuenta de administrador ha sido creada',
                #         f'Tu cuenta de administrador ha sido creada exitosamente. Aquí están tus credenciales:\n\n'
                #         f'Usuario: {usuario.username}\n'
                #         f'Contraseña: {contraseña_aleatoria}\n\n'
                #         f'Por favor, cambia tu contraseña después de iniciar sesión.',
                #         settings.DEFAULT_FROM_EMAIL,
                #         [usuario.username],
                #         fail_silently=False,
                #     )
                # except Exception as e:
                #     print(e)

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