from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PublicacionForm

def realizar_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.save()
            messages.success(request, '¡La publicación se realizó con éxito!')
            return redirect('ver_detalle.html')
        else:
            messages.error(request, '¡No se pudo realizar la publicación! Por favor, corrija los errores indicados.')
    else:
        form = PublicacionForm()
    return render(request, 'realizar_publicacion.html', {'form': form})
