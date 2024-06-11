from django.urls import path
from .Notificacion import views

urlpatterns = [
    path('', views.lista_notificaciones, name='list_notificaciones'),
]