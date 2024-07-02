from django.http import HttpResponse
from django.shortcuts import render
from MDI.decorator import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import *
from Aplicaciones.Modelos.models import Usuario

@login_required
def actualizar_password(request, user_id):
    
    if request.user.id != user_id:
        return HttpResponse('Acceso denegado', status=403)
    
    if (request.method == 'POST'):
        usuario = Usuario.objects.get(id=user_id)
        form = ActualizarPasswordForm(request.POST, user=usuario)
        if form.is_valid():
            newPass = form.cleaned_data['newPassword']
            usuario.set_password(newPass)
            usuario.save()
            update_session_auth_hash(request, usuario) #para evitar que la sesión se cierre luego de actualizar la contraseña
            messages.success(request, "La contraseña se actualizó exitosamente.")
    else:
        form = ActualizarPasswordForm()  
    return render(request, 'GestionUsuarios/actualizar_contraseña.html', {'form': form, 'user_id': user_id})
