from django.contrib import messages
from django.shortcuts import redirect, render
from Aplicaciones.Autenticacion.IniciarSesion.form import LoginForm
from Aplicaciones.GestionUsuarios.RegistrarUsuario.models import Usuario
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            unUsername = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Usuario.objects.get(username=unUsername) #me traigo el usuario con mismo username del form para verificar contraseña
            if user.check_password(password):
                if not user.bloqueado: 
                    login(request, user)
                    return redirect('home')
                else:
                    tiempo_restante = user.cuanto_te_falta()
                    if tiempo_restante > 0:
                        #messages.error(request, f'faltan: {tiempo_restante} horas para desbloquear usuario')
                        messages.error(request, 'Inicio de sesión deshbilitado por 24 hs (En realidad le di 2 minutos)')
                    else:
                        user.desbloquear()
                        login(request, user)
                        return redirect('home')              
            else:
                user.incrementar_ingresos_fallidos()
                messages.error(request, 'Usuario o contraseña no validos. Por favor, intenta de nuevo')
        else:
            messages.error(request, "Usuario o contraseña no validos. Por favor, intenta de nuevo")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

"""
TE LO COMENTO POR LAS DUDAS

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect # Recibe un string (la dir a donde deseamos redirigir)
from django.contrib.auth import login # Encargada de generar la sesion
from django.contrib.auth import authenticate # Encargada de autenticar un usuario

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') #diccionario
        password = request.POST.get('password') #diccionario
        
        # Va a buscar en la BD un usuario que tenga este username y esta contrasenia
        # Si el usuario existe, entonces la funcion devuelve un objeto username
        # Caso contrario, la funcion retorna "None"
        user = authenticate(username=username, password=password)
        if user:
            login(request, user) #Para usar la funcion necesitamos la peticion y el usuario al cual le queremos generar la sesion
            messages.success(request, 'Bienvenido {}'.format(user.username)) #Para usar la funcion necesitamos la peticion y el mensaje
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña no validos. Por favor, intenta de nuevo.')

    return render(request, 'login.html', {
        #context
    })"""