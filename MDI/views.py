from django.shortcuts import render
from django.shortcuts import redirect # Recibe un string (la dir a donde deseamos redirigir)

from django.contrib import messages
from django.contrib.auth import login # Encargada de generar la sesion
from django.contrib.auth import logout # Encargada de cerrar la sesion
from django.contrib.auth import authenticate # Encargada de autenticar un usuario

def home(request): # cuando un cliente realice una consulta sobre la url "home", se va a ejecutar esta funcion :)
    return render(request, 'home.html', {
        #context
    })

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
    })


def logout_view(request):
    logout(request) #La peticion ya conoce la sesion
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('login')

#def prueba(request):
#    return render(request, 'prueba.html')

