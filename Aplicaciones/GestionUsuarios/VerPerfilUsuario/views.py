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

    pubs = Publicacion.objects.filter(autor=request.user).prefetch_related('fotos') 
    ofertas = Oferta.objects.filter(autor=request.user).prefetch_related('fotos')
    return render(request, 'GestionUsuarios/perfilDeUsuario.html',
    {'username': correo,
     'fechaNacimiento': fechaDN,
      'dni': dni,
      'publicaciones': pubs,
      'ofertas': ofertas, }
    )

@login_required
def editar_perfil_view(request, user_id):
    usuario = request.user
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos personales actualizados')
            return redirect('perfil_de_usuario/', user_id)
    else:
        form = EditarPerfilForm(instance=usuario)
    
    context = {
        'form': form,
    }
    return render(request, 'GestionUsuarios/editar_perfil.html', context)