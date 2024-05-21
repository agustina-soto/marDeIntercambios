from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import EditarPublicacionForm, EditarFotoPublicacionForm
from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion, FotoPublicacion

# Importaciones para eliminar una foto
from django.http import JsonResponse
from django.views.decorators.http import require_POST # Asegura que la vista eliminar_foto solo acepte solicitudes HTTP POST


def editar_publicacion(request, publicacion_id):
    # Obtenemos la instancia de la publicación que queremos editar
    publicacion = Publicacion.objects.get(pk=publicacion_id)
    
    # Obtenemos las fotos asociadas a la publicación
    fotos_publicacion = FotoPublicacion.objects.filter(publicacion=publicacion)
    
    if request.method == 'POST':
        # Si la solicitud es un POST, procesamos los datos del formulario
        
        # Creamos instancias de los formularios de edición de publicación y foto
        publicacion_form = EditarPublicacionForm(request.POST, instance=publicacion)
        fotos_nuevas = request.FILES.getlist('foto')  # Obtiene las nuevas fotos subidas
        
        # Verificamos si el formulario es válido
        if publicacion_form.is_valid():

            # Si es válido guardamos los cambios en la base de datos
            publicacion_form.save()
            
            # Si hay fotos nuevas a subir
            if fotos_nuevas:
                for foto in fotos_nuevas:
                    FotoPublicacion.objects.create(publicacion=publicacion, foto=foto) 
                # Para cada foto nueva subida, crea ua instancia y la enlaza con la publicacion

            # Mostramos un mensaje de éxito
            messages.success(request, '¡Se editó la publicación!')
            
            # Redireccionamos a la página de detalle de la publicación
            # return redirect('ver_detalle', pk=publicacion.pk)  # # DES-COMENTAR CUANDO MAITE SUBA EL HTML
    else:
        # Si la solicitud no es un POST, muestra el formulario con los datos actuales de la publicación
        publicacion_form = EditarPublicacionForm(instance=publicacion)
    
    # Renderizamos la plantilla 'editar_publicacion.html' con el formulario y las fotos de la publicación
    return render(request, 'editar_publicacion.html', {
        'publicacion_form': publicacion_form, # Contiene una instancia del formulario EditarPublicacionForm
        'fotos_publicacion': fotos_publicacion, # Contiene las fotos asociadas a la publicación que se está editando
    })

    
# Esta funcion maneja la solicitud de eliminacion de una foto especifica asociada a una publicacion y responde con un JSON indicando el resultado de la operación.
@require_POST
def eliminar_foto(request):
    foto_id = request.POST.get('fotoId') # Obtiene el ID de la foto que se desea eliminar de los datos enviados en la solicitud POST
    if foto_id: # Verifica que el ID de la foto se haya proporcionado en la solicitud
        try:
            foto = FotoPublicacion.objects.get(pk=foto_id) # Intenta obtener la instancia de la foto de la base de datos usando el ID proporcionado
            foto.delete() # Si la foto se encuentra, se elimina de la base de datos. 
            return JsonResponse({'status': 'success'})
        except FotoPublicacion.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Foto no encontrada.'})
    return JsonResponse({'status': 'error', 'message': 'ID de foto no proporcionado.'})