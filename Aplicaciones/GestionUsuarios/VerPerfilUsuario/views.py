from django.shortcuts import render

# Creando los modelos de ver
def perfil_view(request):
    usuario = request.user
    nombreDeUsuario = usuario.username
    fechaDeNacimiento = usuario.fecha_nacimiento
    dniDeUsuario = usuario.dni
    return render(request, 'perfilDeUsuario.html',{ #acá agrego el arreglo de publicaciones
        'username': nombreDeUsuario, 
        'fechaNacimiento': fechaDeNacimiento,
        'dni': dniDeUsuario
        }
    )