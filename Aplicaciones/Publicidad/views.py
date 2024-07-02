from datetime import date
import json
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import Publicidad
from .forms import PublicidadForm
from django.contrib import messages

"""def programar_publicidad(request):
    if request.method == 'POST':
        publicidad_form = PublicidadForm(request.POST)
        foto_form = FotoPublicidadForm(request.POST, request.FILES)

        if publicidad_form.is_valid():
            fotos = request.FILES.getlist('foto')
            if len(fotos) != 1:
                foto_form.add_error('foto', 'Debes subir exactamente 3 fotos.')
            else:
                if foto_form.is_valid():
                    try:
                        publicidad = publicidad_form.save()
                        for foto in fotos:
                            FotoPublicidad.objects.create(publicidad=publicidad, foto=foto)
                        messages.success(request, '¡Se programó la publicidad con éxito!')
                        return redirect('listar_publicidades')  # Redirige a la lista de publicidades realizadas
                    
                    except Exception as e:
                        publicidad_form.add_error(None, str(e))
                else:
                    messages.error(request, '¡No se pudo programar la publicidad! Verifique las fotos subidas.')
        else:
            messages.error(request, '¡No se pudo programar la publicidad! Verifique los datos ingresados.')
    else:
        publicidad_form = PublicidadForm()
        foto_form = FotoPublicidadForm()

    return render(request, 'Publicidad/programar_publicidad.html', {
        'publicidad_form': publicidad_form,
        'foto_form': foto_form,
    })"""


def programar_publicidad(request):
    if request.method == 'POST':
        publicidad_form = PublicidadForm(request.POST, request.FILES)

        if publicidad_form.is_valid():
            nueva_publicidad = publicidad_form.save()  # Guarda la instancia de Publicidad con la fecha seleccionada
            
            messages.success(request, '¡Se programó la publicidad con éxito!')
            return redirect('listar_publicidades')  # Redirige a la lista de publicidades programadas
        else:
            messages.error(request, '¡No se pudo programar la publicidad! Verifique los datos ingresados.')

    else:
        publicidad_form = PublicidadForm()
    
    # Obtener todas las fechas ocupadas y convertirlas a cadenas
    fechas_ocupadas = Publicidad.objects.values_list('fecha', flat=True)

    return render(request, 'Publicidad/programar_publicidad.html', {
        'publicidad_form': publicidad_form,
        'fechas_ocupadas': fechas_ocupadas  
    })

def listar_publicidades(request):

    publicidades = Publicidad.objects.all()
    publicidades_futuras = publicidades.filter(fecha__gt=date.today())
    publicidades_pasadas = publicidades.filter(fecha__lt=date.today())

    context = {
        'publicidades_futuras': publicidades_futuras,
        'publicidades_pasadas': publicidades_pasadas,
    }

    return render(request, 'Publicidad/listar_publicidades.html', context)


def mostrar_publicidad_central(request):
    hoy = timezone.now().date()
    publicidad = Publicidad.objects.filter(fecha=hoy).first()
    print(hoy)
    return render(request, 'Publicidad/banner_central.html', {'publicidad': publicidad, })


def mostrar_publicidad_lateral(request):

    hoy = timezone.now().date()
    publicidad = Publicidad.objects.filter(fecha=hoy).first()

    return render(request, 'Publicidad/banner_lateral.html', {'publicidad': publicidad,})


"""def editar_publicidad(request, pk):

    publicidad = get_object_or_404(Publicidad, pk=pk)

    if request.method == 'POST':
        publicidad_form = PublicidadForm(request.POST, request.FILES, instance=publicidad)
        if publicidad_form.is_valid():
            publicidad_form.save()
            return redirect('listar_publicidades')
    else:
        publicidad_form = PublicidadForm(instance=publicidad)

    return render(request, 'Publicidad/editar_publicidad.html', {'publicidad_form': publicidad_form})"""

def editar_publicidad(request, id):
    publicidad = get_object_or_404(Publicidad, id=id)

    if request.method == 'POST':
        publicidad_form = PublicidadForm(request.POST, request.FILES, instance=publicidad)
        if publicidad_form.is_valid():
            # Eliminar fotos existentes marcadas para eliminación
            fotos_central_a_eliminar = request.POST.get('fotos_central_a_eliminar').split(',')
            fotos_lateral_a_eliminar = request.POST.get('fotos_lateral_a_eliminar').split(',')

            if 'eliminar_foto_central' in fotos_central_a_eliminar and publicidad.foto_central:
                publicidad.foto_central.delete(save=False)
                publicidad.foto_central = None

            if 'eliminar_foto_lateral' in fotos_lateral_a_eliminar and publicidad.foto_lateral:
                publicidad.foto_lateral.delete(save=False)
                publicidad.foto_lateral = None

            # Guardar nuevas fotos y el formulario actualizado
            if 'foto_central' in request.FILES:
                publicidad.foto_central = request.FILES['foto_central']
            if 'foto_lateral' in request.FILES:
                publicidad.foto_lateral = request.FILES['foto_lateral']

            # Guardar el formulario actualizado
            publicidad_form.save()

            return redirect('listar_publicidades')
    else:
        publicidad_form = PublicidadForm(instance=publicidad)

    # Obtener todas las fechas ocupadas y convertirlas a cadenas
    fechas_ocupadas = Publicidad.objects.values_list('fecha', flat=True)

    return render(request, 'publicidad/editar_publicidad.html', {'publicidad_form': publicidad_form, 'fechas_ocupadas': fechas_ocupadas})



def eliminar_publicidad(request, pk):
    publicidad = get_object_or_404(Publicidad, pk=pk)

    if request.method == 'POST':
        publicidad.estado = 'eliminada'
        publicidad.fecha = None
        publicidad.save()
        return redirect('listar_publicidades')
    
    return render(request, 'Publicidad/listar_publicidades.html', {'publicidades': Publicidad.objects.all()})

