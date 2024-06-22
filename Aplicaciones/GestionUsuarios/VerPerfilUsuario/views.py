from django.shortcuts import redirect, render
from django.contrib import messages
from Aplicaciones.GestionUsuarios.VerPerfilUsuario.forms import ActualizarPassForm, EditarPerfilForm
from Aplicaciones.Modelos.models import Oferta, Publicacion
from MDI.decorator import login_required
from django.contrib.auth.decorators import login_required # por que hay 2 login required importados??
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse, reverse_lazy

@login_required 
def perfil_view(request):
    #Podría haber mandado un usuario completo, pero no lo contemplé, después lo arreglo
    usuario = request.user
    correo = usuario.username
    fechaDN = usuario.fecha_nacimiento
    dni = usuario.dni
    #El ver perfil de la h.u estaba raro, por el momento agregé para que un usuario autenticado vea su perfil
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
def editar_perfil_view(request):
    usuario = request.user
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos personales actualizados')
            return redirect('perfil_de_usuario')
    else:
        form = EditarPerfilForm(instance=usuario)
    
    context = {
        'form': form,
    }
    return render(request, 'GestionUsuarios/editar_perfil.html', context)


class ActualizarPassFormView(PasswordChangeView):
    form_class = ActualizarPassForm
    template_name = 'GestionUsuarios/actualizarContraseña.html'
    success_url = reverse_lazy('perfil_de_usuario')

    def form_valid(self, form):
        # Guarda la contraseña y muestra un mensaje de éxito
        form.save()
        messages.success(self.request, 'Contraseña actualizada exitosamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Muestra un mensaje de error si no se pudo actualizar la contraseña
        messages.error(self.request, 'No se pudo actualizar la contraseña. Por favor, inténtelo de nuevo.')
        return super().form_invalid(form)