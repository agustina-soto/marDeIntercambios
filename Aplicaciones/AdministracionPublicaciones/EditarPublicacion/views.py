from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EditarPublicacionForm, EditarFotoPublicacionForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion, FotoPublicacion

def editar_publicacion(request, publicacion_id):
    # Obtenemos la instancia de la publicación que queremos editar
    publicacion = Publicacion.objects.get(pk=publicacion_id)
    
    # Obtenemos las fotos asociadas a la publicación
    fotos_publicacion = FotoPublicacion.objects.filter(publicacion=publicacion)
    
    if request.method == 'POST':
        # Si la solicitud es un POST, procesamos los datos del formulario
        
        # Creamos instancias de los formularios de edición de publicación y foto
        publicacion_form = EditarPublicacionForm(request.POST, instance=publicacion)
        foto_form = EditarFotoPublicacionForm(request.POST, request.FILES, instance=publicacion)
        
        # Verificamos si ambos formularios son válidos
        if publicacion_form.is_valid() and foto_form.is_valid():
            # Si son válidos, guardamos los cambios en la base de datos
            publicacion_form.save()
            foto_form.save()
            
            # Mostramos un mensaje de éxito
            messages.success(request, '¡Se editó la publicación!')
            
            # Redireccionamos a la página de detalle de la publicación
            #return redirect('ver_detalle.html', , pk=publicacion.pk) # DES-COMENTAR CUANDO MAITE SUBA EL HTML
    else:
        # Si la solicitud no es un POST, mostramos los formularios con los datos actuales de la publicación
        publicacion_form = EditarPublicacionForm(instance=publicacion)
        foto_form = EditarFotoPublicacionForm(instance=publicacion)
    
    # Renderizamos la plantilla 'editar_publicacion.html' con los formularios y las fotos de la publicación
    return render(request, 'editar_publicacion.html', {
        'publicacion_form': publicacion_form,
        'foto_form': foto_form,
        'fotos_publicacion': fotos_publicacion,
        })
    # publicacion_form y foto_form contienen instancias de los formularios EditarPublicacionForm y EditarFotoPublicacionForm (respectivamente)
    # fotos_publicacion contiene las fotos asociadas a la publicación que se está editando
