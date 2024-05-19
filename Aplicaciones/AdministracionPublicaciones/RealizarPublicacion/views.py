from django.shortcuts import render, redirect
from django.contrib import messages

from .models import FotoPublicacion
from .forms import PublicacionForm, FotoPublicacionForm


def realizar_publicacion(request):
    if request.method == 'POST':
        publicacion_form = PublicacionForm(request.POST)
        foto_form = FotoPublicacionForm(request.POST, request.FILES)
        
        if publicacion_form.is_valid() and foto_form.is_valid():
            publicacion = publicacion_form.save()
            fotos = request.FILES.getlist('foto')
            for foto in fotos:
                FotoPublicacion.objects.create(publicacion=publicacion, foto=foto) # Hace el enlace entre Publicacion y FotoPublicacion
            messages.success(request, '¡La publicación se realizó con éxito!')
            #return redirect('ver_detalle.html', , pk=publicacion.pk) # DES-COMENTAR CUANDO MAITE SUBA EL HTML
        else:
            messages.error(request, '¡No se pudo realizar la publicación! Por favor, corrija los errores indicados.')
    else:
        publicacion_form = PublicacionForm()
        foto_form = FotoPublicacionForm()
    
    return render(request, 'realizar_publicacion.html', {'publicacion_form': publicacion_form, 'foto_form': foto_form})
