from django.shortcuts import render
from MDI.decorator import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import *

@login_required
def actualizar_password(request):
    if (request.method == 'POST'):
        form = ActualizarPasswordForm(request.POST, user=request.user)
        if form.is_valid():
            usuario = request.user
            newPass = form.cleaned_data['newPassword']
            usuario.set_password(newPass)
            usuario.save()
            update_session_auth_hash(request, request.user) #para evitar que la sesión se cierre luego de actualizar la contraseña
            messages.success(request, "La contraseña se actualizó exitosamente.")
    else:
        form = ActualizarPasswordForm()   
    return render(request, 'GestionUsuarios/actualizar_contraseña.html', {'form': form})
