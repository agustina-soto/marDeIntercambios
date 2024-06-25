from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm
from .models import *
from MDI.decorator import login_required, user_passes_test_superuser

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
        form = RegistroForm(request.POST) #Se verifcan datos dentro del form y se genera instancia de un usuario para su registro
        if form.is_valid(): #si no ocurrió ningún error...
            try:
                form.save()
                #usuario = form.save() 
                #login(request, usuario) #No sé si hace falta loguear al usuario que se registre, la h.u no lo especifica
                messages.success(request, "Usuario Administrador Registrado con éxito!")
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = RegistroForm()
    return render(request, 'GestionUsuarios/registro_administrador.html', {'form': form})