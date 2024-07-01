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

    return render(request, 'publicidad/programar_publicidad.html', {
        'publicidad_form': publicidad_form,
        'fechas_ocupadas': fechas_ocupadas  
    })

def listar_publicidades(request):

    publicidades = Publicidad.objects.all()
    context = {'publicidades': publicidades}

    return render(request, 'publicidad/listar_publicidades.html', context)


def mostrar_publicidad_central(request):
    hoy = timezone.now().date()
    publicidad = Publicidad.objects.filter(fecha=hoy).first()
    return render(request, 'publicidad/banner_central.html', {'publicidad': publicidad})


def mostrar_publicidad_lateral(request):

    hoy = timezone.now().date()
    publicidad = Publicidad.objects.filter(fecha=hoy).first()
    return render(request, 'publicidad/banner_lateral.html', {'publicidad': publicidad,})


def editar_publicidad(request, pk):
    publicidad = get_object_or_404(Publicidad, pk=pk)

    if request.method == 'POST':
        form = PublicidadForm(request.POST, instance=publicidad)
        if form.is_valid():
            form.save()
            return redirect('listar_publicidades')
    else:
        form = PublicidadForm(instance=publicidad)

    return render(request, 'publicidad/editar_publicidad.html', {'form': form})

def eliminar_publicidad(request, pk):
    pass

"""
ESTA ENTRAR EN CONFLICTO CON LA FECHA XQ SI NO LA ELIMINO DE LA BASE DE DATOS QUEDA COMO OCUPADA 

def eliminar_publicidad(request, pk):
    publicidad = get_object_or_404(Publicidad, pk=pk)

    if request.method == 'POST':
        publicidad.delete()
        return redirect('listar_publicidades')
    
    return render(request, 'Publicidad/listar_publicidades.html', {'publicidades': Publicidad.objects.all()})
"""
