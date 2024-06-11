from django.urls import path

from .views import ver_historial_intercambios;

urlpatterns = [
    path('ver_historial_intercambios/', ver_historial_intercambios, name='ver_historial_intercambios'),
]
