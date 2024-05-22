from django.shortcuts import render
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required

@login_required 
def perfil_view(request):
    usuario = request.user
    correo = usuario.username
    fechaDN = usuario.fecha_nacimiento
    dni = usuario.dni
    pubs = Publicacion.objects.filter(usuario=request.user).prefetch_related('fotos')
    return render(request, 'perfilDeUsuario.html',
    {'username': correo,
     'fechaNacimiento': fechaDN,
      'dni': dni,
      'publicaciones': pubs
     }
    )