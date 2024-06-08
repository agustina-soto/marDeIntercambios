from django.shortcuts import render
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required

@login_required 
def perfil_view(request):
    #Podría haber mandado un usuario completo, pero no lo contemplé, después lo arreglo
    usuario = request.user
    correo = usuario.username
    fechaDN = usuario.fecha_nacimiento
    dni = usuario.dni
    #El ver perfil de la h.u estaba raro, por el momento agregé para que un usuario autenticado vea su perfil
    pubs = Publicacion.objects.filter(usuario=request.user).prefetch_related('fotos') 
    return render(request, 'GestionUsuarios/perfilDeUsuario.html',
    {'username': correo,
     'fechaNacimiento': fechaDN,
      'dni': dni,
      'publicaciones': pubs
     }
    )