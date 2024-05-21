from django.shortcuts import render, redirect
from django.contrib import messages

from .models import FotoPublicacion
from .forms import PublicacionForm, FotoPublicacionForm

from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required #Luck: creé el decorator en MDI para reutilizarlo

@login_required 
def realizar_publicacion(request):
    if request.method == 'POST':
        # Instancia los formularios con los datos proporcionados por el usuario
        publicacion_form = PublicacionForm(request.POST)
        foto_form = FotoPublicacionForm(request.POST, request.FILES)

        # Verifica si ambos formularios son válidos
        if publicacion_form.is_valid() and foto_form.is_valid():
            
            # Guarda la instancia de Publicacion y obtener la lista de fotos
            publicacion = publicacion_form.save()
            fotos = request.FILES.getlist('foto')
            
            # Crea una instancia de FotoPublicacion para cada foto cargada, enlazándola con la publicación
            for foto in fotos:
                FotoPublicacion.objects.create(publicacion=publicacion, foto=foto) # Establece la relación entre Publicacion y FotoPublicacion
            
            # Muestra un mensaje de éxito y redireccionar a algún lugar apropiado
            messages.success(request, '¡La publicación se realizó con éxito!')
            return redirect('ver_detalle', pk=publicacion.pk)
        
        else:
            # Muestra un mensaje de error si los formularios no son válidos
            messages.error(request, '¡No se pudo realizar la publicación! Por favor, corrija los errores indicados.')
    else:
        # Si la solicitud no es POST, crea instancias de formularios vacíos
        publicacion_form = PublicacionForm()
        foto_form = FotoPublicacionForm()
    
    # Renderiza la plantilla con los formularios
    return render(request, 'realizar_publicacion.html', {'publicacion_form': publicacion_form, 'foto_form': foto_form})
