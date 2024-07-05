from django.contrib import messages
from django.shortcuts import redirect, render # Recibe un string (la dir a donde deseamos redirigir)
from Aplicaciones.Autenticacion.IniciarSesion.form import LoginForm
from Aplicaciones.GestionUsuarios.RegistrarUsuario.models import Usuario
from datetime import timedelta
from django.contrib.auth import login  # Encargada de generar la sesion

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():          
            unUsername = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Usuario.objects.get(username=unUsername) #Me traigo el usuario con mismo username de la db para verificar contraseña
            if (no_esta_eliminado(request, user)) and (no_esta_baneado(request,user)):
                if user.check_password(password):           
                    return inicio_sesion_exitoso(request, user, form)
                else:
                    return inicio_sesion_fallido(request, user, form)         
        else:
            #No se encontró nombre de usuario en BD
            messages.error(request, 'Usuario o contraseña no válidos. Por favor, intenta de nuevo')
    else:
        form = LoginForm()
    return render(request, 'Autenticacion/login.html', {'form': form})

def no_esta_baneado(request, usuario):
    if (usuario.estado_cuenta == 'baneado'):
        if (fin_de_baneo(usuario)):
            usuario.desbloquear()
            usuario.is_active = True
            usuario.estado_cuenta = 'activo'
            return True
        else:
            context = f'Usuario baneado el día {usuario.fecha_bloqueo.strftime("%d-%m-%Y")}, su cuenta se desbloqueará el día {(usuario.fecha_bloqueo + timedelta(days=7)).strftime("%d-%m-%Y")}'
            messages.error(request, context)
            return False
    return True

def no_esta_eliminado(request, usuario):
    if (usuario.estado_cuenta == 'Deshabilitado'):
        messages.error(request, 'La cuenta a la que estás intentando ingresar se encuentra deshabilitada')
        return False
    return True

#Manejo inicio de sesión fallido
def inicio_sesion_fallido(request, user, form):
    if not user.bloqueado or fin_de_baneo(user):
        if user.bloqueado:
            user.desbloquear()
        fallo_iniciar_sesion(request, user)
    else:
        messages.error(request, 'Inicio de sesión deshabilitado por 24 hs')
    return render(request, 'Autenticacion/login.html', {'form': form})

def fallo_iniciar_sesion(request, user):
    user.incrementar_ingresos_fallidos()
    messages.error(request, 'Usuario o contraseña no válidos. Por favor, intenta de nuevo')  

#Manejo inicio de sesión exitoso

def inicio_sesion_exitoso(request, user, form):
    if not user.bloqueado or fin_de_bloqueo(user):
        if user.bloqueado:
            user.desbloquear()
        iniciar_sesion(request, user)
        return redirect('home')
    else:
        messages.error(request, 'Inicio de sesión deshabilitado por 24 hs')
    return render(request, 'Autenticacion/login.html', {'form': form})
    
def iniciar_sesion(request, user):
    user.resetear_ingresos_fallidos()
    login(request, user)
    messages.success(request, f'Bienvenido {user.username}')

#Manejo del tiempo restante

def fin_de_bloqueo(user):
    return user.cuanto_te_falta_por_bloqueo() < 0

def fin_de_baneo(user):
    return user.cuanto_te_falta_por_baneo() < 0