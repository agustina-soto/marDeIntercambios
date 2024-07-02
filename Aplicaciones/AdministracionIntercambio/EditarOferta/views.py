"""from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from Aplicaciones.AdministracionIntercambio.RealizarOferta.models import Oferta, FotoOferta
from .forms import EditarOfertaForm

#agregar que solo puedan acceder user logeados
def editar_oferta (request, oferta_id):
    # Obtenemos la instancia de la oferta que queremos editar a partir del ID proporcionado
    oferta = get_object_or_404(Oferta, pk=oferta_id) #Oferta.objects.get(pk=oferta_id)
    # Obtenemos la publicación asociada a la oferta
    publicacion = oferta.publicacion 
    # Obtenemos todas las fotos asociadas a esta oferta
    fotos_oferta = FotoOferta.objects.filter(oferta=oferta)

    if request.method == 'POST':
        # Creamos una instancia del formulario con los datos enviados y la publicación existente
        oferta_form = EditarOfertaForm(request.POST, instance=oferta, publicacion=publicacion)
        # Obtenemos las nuevas fotos que se han subido
        fotos_nuevas = request.FILES.getlist('foto')
        # Obtenemos la lista de IDs de las fotos que se han marcado para eliminar
        fotos_a_eliminar_ids = [id for id in request.POST.get('fotos_a_eliminar', '').split(',') if id]

        if oferta_form.is_valid():
            # Guardar la oferta con los nuevos datos
            oferta_form.save()
            
            # Eliminar las fotos marcadas para eliminación
            for foto_id in fotos_a_eliminar_ids:
                try:
                    foto_a_eliminar = FotoOferta.objects.get(pk=foto_id)
                    foto_a_eliminar.delete()
                except FotoOferta.DoesNotExist:
                    pass

            # Agregar las nuevas fotos subidas
            for foto in fotos_nuevas:
                FotoOferta.objects.create(oferta=oferta, foto=foto)

            messages.success(request, '¡Se editó la oferta!')
            return redirect('ver_detalle_oferta', pk=oferta.pk)
        else:
            # Si el formulario no es válido, mostramos un mensaje de error
            messages.error(request, '¡No se pudo editar la oferta!')
    
    else:
        # Si la solicitud no es POST, creamos una instancia del formulario con los datos actuales de la publicación
        oferta_form = EditarOfertaForm(instance=oferta, publicacion=publicacion)

    # Renderizamos la plantilla 'editar_oferta.html' con el formulario y las fotos de la oferta
    return render(request, 'AdminitracionIntercambio/editar_oferta.html', {
        'oferta_form': oferta_form,
        'fotos_oferta': fotos_oferta,
    })"""


