from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from Aplicaciones.GestionUsuarios.VerPerfilUsuario.forms import EditarPerfilForm
from Aplicaciones.Modelos.models import Oferta, Publicacion, Usuario
from MDI.decorator import login_required
from django.contrib.auth.decorators import login_required # por que hay 2 login required importados??

@login_required 
def perfil_view(request, user_id):
   
    if request.user.id != user_id:
        return HttpResponse('No tienes permiso para ver el perfil de otro usuario.', status=403)
    
    usuario = Usuario.objects.get(id=user_id)
    correo = usuario.username
    fechaDN = usuario.fecha_nacimiento
    dni = usuario.dni

    # Agarro todas las publicaciones y me quedo con las primeras 3
    todas_publicaciones = Publicacion.objects.filter(autor=request.user).prefetch_related('fotos')
    publicaciones = todas_publicaciones[:3]

    # Agarro todas las ofertas y me quedo con las primeras 3
    todas_ofertas = Oferta.objects.filter(autor=request.user).prefetch_related('fotos')
    ofertas = todas_ofertas[:3]

    return render(request, 'GestionUsuarios/perfilDeUsuario.html', {
        'user_id': user_id,
        'username': correo,
        'fechaNacimiento': fechaDN,
        'dni': dni,
        'publicaciones': publicaciones,
        'todas_publicaciones_count': todas_publicaciones.count(),  # Envia la cantidad total de publicaciones
        'ofertas': ofertas,
    })


@login_required
def editar_perfil_view(request, user_id):
    
    if request.user.id != user_id:
        return HttpResponse('Acceso denegado', status=403)
    
    usuario = Usuario.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos personales actualizados')
            return redirect('perfil_de_usuario', user_id)
    else:
        form = EditarPerfilForm(instance=usuario)
    
    context = {
        'user_id': user_id,
        'form': form,
    }
    return render(request, 'GestionUsuarios/editar_perfil.html', context)


def ver_todas_mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(autor=request.user)
    context = {
        'publicaciones': publicaciones,
    }
    return render(request, 'VisualizacionPublicaciones/ver_todas_mis_publicaciones.html', context)


def ver_todas_mis_ofertas(request):
    ofertas = Oferta.objects.filter(autor=request.user)
    context = {
        'ofertas': ofertas,
    }
    return render(request, 'Ofertas/ver_todas_mis_ofertas.html', context)