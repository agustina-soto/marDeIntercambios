from django.shortcuts import render, redirect
from .forms import PublicacionForm

def realizar_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ver_detalle.html')
    else:
        form = PublicacionForm()
    return render(request, 'realizar_publicacion.html', {'form': form})