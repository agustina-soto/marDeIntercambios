from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from MDI.decorator import login_required #Luck: creé el decorator en MDI para reutilizarlo
from django.contrib.auth.decorators import user_passes_test
from MDI.decorator import user_passes_test_superuser #Gio: creé el decorator en MDI para reutilizarlo

@login_required 
@user_passes_test_superuser
def ver_publicaciones_para_validar(request):
  
    # Renderiza la plantilla con los formularios
    return render(request, 'AdministracionPublicaciones/ver_publicaciones_para_validar.html')
