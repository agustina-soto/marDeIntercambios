import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, RegistroFormAdministrador
from .models import *
from MDI.decorator import login_required, user_passes_test_superuser
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

@login_required 
@user_passes_test_superuser
def banear_usuario (request, usuario_id):

    print("Baneamos al usuario " + str(usuario_id))


    return redirect("ver_lista_usuarios_baneados")