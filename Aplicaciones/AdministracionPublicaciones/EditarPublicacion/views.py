from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Publicacion, FotoPublicacion, Oferta
from .forms import EditarPublicacionForm

def editar_publicacion(request, publicacion_id):
    # Obtenemos la instancia de la publicación que queremos editar a partir del ID proporcionado
    publicacion = Publicacion.objects.get(pk=publicacion_id)

    # Verificamos si la publicación tiene ofertas
    if Oferta.objects.filter(publicacion=publicacion).exists():
        # Si tiene ofertas, mostramos un mensaje de error y redirigimos a la vista de detalle de la publicación
        messages.error(request, '¡No puedes editar una publicación que ya tiene ofertas recibidas!')
        ruta = "/publicacion/ver-publicacion/ver_detalle/" + str(publicacion.id) 
        return redirect(ruta, pk=publicacion.pk) #NO CUENTO CON VER DETALLE

    # Obtenemos todas las fotos asociadas a esta publicación
    fotos_publicacion = FotoPublicacion.objects.filter(publicacion=publicacion)

    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos enviados y la publicación existente
        publicacion_form = EditarPublicacionForm(request.POST, instance=publicacion)
        # Obtenemos las nuevas fotos que se han subido
        fotos_nuevas = request.FILES.getlist('foto')
        # Obtenemos la lista de IDs de las fotos que se han marcado para eliminar
        fotos_a_eliminar_ids = [id for id in request.POST.get('fotos_a_eliminar', '').split(',') if id]

        if publicacion_form.is_valid():
            # Calculamos la cantidad de fotos que quedarán después de las eliminaciones y adiciones
            fotos_restantes = fotos_publicacion.count() - len(fotos_a_eliminar_ids) + len(fotos_nuevas)

            if fotos_restantes == 0:
                # Si no quedan fotos, mostramos un mensaje de error
                messages.error(request, '¡Debes subir por lo menos una foto!')
            else:
                # Guardar la publicación con los nuevos datos
                publicacion_form.save()

                # Eliminar las fotos marcadas para eliminación
                for foto_id in fotos_a_eliminar_ids:
                    try:
                        foto_a_eliminar = FotoPublicacion.objects.get(pk=foto_id)
                        foto_a_eliminar.delete()
                    except FotoPublicacion.DoesNotExist:
                        pass

                # Agregar las nuevas fotos subidas
                for foto in fotos_nuevas:
                    FotoPublicacion.objects.create(publicacion=publicacion, foto=foto)

                # Mostrar un mensaje de éxito y redirigir a la vista de detalle de la publicación
                messages.success(request, '¡Se editó la publicación!')
                ruta = "/publicacion/ver-publicacion/ver_detalle/" + str(publicacion.id)
                return redirect(ruta, pk=publicacion.pk) #NO CUENTO CON VER_DETALLE
        else:
            # Si el formulario no es válido, mostramos un mensaje de error
            messages.error(request, '¡No se pudo editar la publicación! Por favor, corrija los errores indicados.')

    else:
        # Si la solicitud no es POST, creamos una instancia del formulario con los datos actuales de la publicación
        publicacion_form = EditarPublicacionForm(instance=publicacion)

    # Renderizamos la plantilla 'editar_publicacion.html' con el formulario y las fotos de la publicación
    return render(request, 'AdministracionPublicaciones/editar_publicacion.html', {
        'publicacion_form': publicacion_form,
        'fotos_publicacion': fotos_publicacion,
    })