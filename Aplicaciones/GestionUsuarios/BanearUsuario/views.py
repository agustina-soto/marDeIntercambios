import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, RegistroFormAdministrador
from Aplicaciones.Modelos.models import *
from MDI.decorator import login_required, user_passes_test_superuser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

@login_required 
@user_passes_test_superuser
def banear_usuario (request, usuario_id):

    # Traemos todas las publicaciones del usuario
    publicacionesUsuario = Publicacion.objects.filter(autor=usuario_id)

    # Recorremos cada una de las publicaciones y procesamos sus datos para la eliminación
    for pubs in publicacionesUsuario:    
        # Rechaza todas las ofertas asociadas a esta publicación
        Oferta.objects.filter(publicacion=pubs).update(estado='rechazada')
        # Rechaza los intercambios activos asociadas a esta publicación
        Intercambios.objects.filter(publicacion=pubs, estado="pendiente").update(estado="rechazado")

    #     # Defino como None su oferta aceptada y asigno estado como eliminada
        pubs.oferta_aceptada = None
        pubs.estado = "eliminada"
        pubs.save()

    # Rechazo todas las ofertas del usuario
    ofertasUsuario = Oferta.objects.filter(autor=usuario_id)
    for of in ofertasUsuario:
        pubsDeOferta = Publicacion.objects.filter(oferta_aceptada=of)

        for pubs in pubsDeOferta:
            Intercambios.objects.filter(publicacion=pubs, estado="pendiente").update(estado="rechazado")
            pubs.oferta_aceptada = None
            pubs.save()

        of.estado = "rechazada"
        of.save()



    usuario = Usuario.objects.get(id=usuario_id)

    usuario.estado_cuenta = "baneado"
    usuario.bloquear()

    print("Baneamos al usuario " + str(usuario_id))
    return redirect("ver_lista_usuarios_baneados")

@login_required 
@user_passes_test_superuser
def desbanear_usuario (request, usuario_id):

    # Traemos todas las publicaciones del usuario
    publicacionesUsuario = Publicacion.objects.filter(autor=usuario_id)

    # Recorremos cada una de las publicaciones y procesamos sus datos para la eliminación
    for pubs in publicacionesUsuario:    

        pubs.estado = "aceptada"
        pubs.save()


    usuario = Usuario.objects.get(id=usuario_id)

    usuario.estado_cuenta = "activo"
    usuario.desbloquear()


    print("Desbaneamos al usuario " + str(usuario_id))
    return redirect("ver_lista_usuarios")