from django.urls import path
from . import views

urlpatterns = [
    path('preguntas_frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('politicas_privacidad/', views.politicas_privacidad, name='politicas_privacidad'),
    path('terminos_y_condiciones/', views.terminos_y_condiciones, name='terminos_y_condiciones'),
    path('contacto_puerto_aventura/', views.contacto_puerto_aventura, name='contacto_puerto_aventura'),
    path('informacion_puerto_aventura/', views.informacion_puerto_aventura, name='informacion_puerto_aventura'),
    path('contacto_equipo_desarrollo/', views.contacto_equipo_desarrollo, name='contacto_equipo_desarrollo'),
]
