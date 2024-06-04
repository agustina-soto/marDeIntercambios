from django.shortcuts import render
from django.http import HttpResponse, Http404
from Aplicaciones.Modelos.models import Publicacion, Oferta

def ver_ofertas(request, id):
    try:
        publicacion = Publicacion.objects.get(id=id)
    except Publicacion.DoesNotExist:
        raise Http404("La publicación no existe")
    
    ofertas = Oferta.objects.filter(publicacion=publicacion)
    return render(request, 'Ofertas/ver_ofertas.html', {'publicacion': publicacion, 'ofertas': ofertas})
