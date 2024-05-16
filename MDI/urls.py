"""
URL configuration for MDI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views 
from Aplicaciones.GestionUsuarios.RegistrarUsuario.views import *

urlpatterns = [
    path('', views.home, name='home'), #base
    path('registro/', registro, name='registro'),
    path('registro/exitoRegistro/', exito_registro, name='exito_registro'),
    path('usuarios/login', views.login, name='login'),
    path('admin/', admin.site.urls),
    path('prueba/', views.prueba, name='prueba'),
    path('prueba2/', views.prueba2, name='prueba2'),
]
