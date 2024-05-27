from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import *

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST) #Se verifcan datos dentro del form y se genera instancia de un usuario para su registro
        if form.is_valid(): #si no ocurrió ningún error...
            try:
                form.save()
                #usuario = form.save() 
                #login(request, usuario) #No sé si hace falta loguear al usuario que se registre, la h.u no lo especifica
                return redirect('exito_registro')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = RegistroForm()
    return render(request, 'GestionUsuarios/registro.html', {'form': form})

def exito_registro(request):
    return render(request, 'GestionUsuarios/exitoRegistro.html')