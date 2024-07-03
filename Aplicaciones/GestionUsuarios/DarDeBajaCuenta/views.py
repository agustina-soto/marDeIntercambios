from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from MDI.decorator import login_required
from Aplicaciones.Modelos.models import Usuario

@login_required
def dar_de_baja(request, user_id):

    if request.user.id != user_id:
        return HttpResponse('Acceso denegado', status=403)
    
    if (request.method == 'POST'):
        usuario = Usuario.objects.get(id=user_id)
        motivo = request.POST.get('motivo')
        ok = True;
        if (not motivo):
            messages.error(request, "el campo motivo no debe quedar vacío. Debe completarse el motivo de la eliminación para proceder con la desactivación de la cuenta")
            ok = False
        else:
            if (tiene_oferta_propia_aceptada(usuario)):
                messages.error(request, "No pueden eliminarse cuentas con ofertas aceptadas. Debe comunicarse con administración para proceder con la baja de la cuenta")
                ok = False
            if (tiene_oferta_ajena_aceptada(usuario)):
                messages.error(request, " No pueden eliminarse cuentas con ofertas aceptadas. Debes cancelar la oferta aceptada para proceder con la baja de la cuenta")
                ok = False
        if (ok):
            eliminar_cuenta(usuario, motivo)
            messages.success(request, "La cuenta ha sido dada de baja")
            return redirect('login')
    return render(request, "GestionUsuarios/dar_de_baja_cuenta.html")

def tiene_oferta_ajena_aceptada(usuario):
    return usuario.publicaciones.filter(oferta_aceptada__isnull=False).exists()

def tiene_oferta_propia_aceptada(usuario):
    return usuario.ofertas_autor.filter(estado="aceptada").exists()

def eliminar_cuenta(usuario, motivo):
    usuario.is_active = False
    usuario.estado_cuenta = 'Deshabilitado' #Estaba en el modelo, no quise tocarlo por si se usaba en otra parte
    usuario.motivo = motivo

    for publicacion in usuario.publicaciones.all():
        publicacion.estado = 'Eliminada'
        publicacion.save()
    
    for oferta in usuario.ofertas_autor.all():
        oferta.estado = 'Eliminada'
        oferta.save()

    usuario.save()