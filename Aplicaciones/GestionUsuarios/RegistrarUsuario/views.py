from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UsuarioRegistradoForm
from .models import UsuarioRegistrado

def registro(request):
    if request.method == 'POST': #si aprieto registrar...
        form = UsuarioRegistradoForm(request.POST) #creo un formulario con los datos recibidos
        if form.is_valid(): #compruebo validaciones def clean_... hechas en el forms
            usuario = form.save()
            return redirect('exito_registro')
    else:
        form = UsuarioRegistradoForm() #retorno formulario con campos fallidos vacíos
    return render(request, 'registro.html', {'form': form})

def base(request):
    return render(request, 'base.html')

def exito_registro(request):
    return render(request, 'exitoRegistro.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get['email']
        contraseña = request.POST.get['password']  # Changed 'password' to 'contraseña'

        usuario = authenticate(request, email=email, password=password)
        print('ENTRA')
        print(usuario)
        if usuario is not None:
            # Busca al usuario en la base de datos por correo electrónico
            usuario_autenticado = UsuarioRegistrado.objects.get(email=email)
        
            login(request, usuario_autenticado)  # Inicia sesión con el usuario autenticado
            return redirect('home')  # Cambiar "home" por la URL de tu página de inicio
        else:
            mensaje_error = "Email o contraseña incorrectos."
    else:
        mensaje_error = None

    contexto = {
        'mensaje_error': mensaje_error
    }
    return render(request, 'login.html', contexto)