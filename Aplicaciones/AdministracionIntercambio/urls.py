from django.urls import path
from .RealizarOferta import views
from .EditarOferta import views as views_editar

urlpatterns= [
    path('realizar_oferta/<int:publicacion_id>/', views.realizar_oferta, name='realizar_oferta'),
    path('ver_detalle_oferta/<int:pk>/', views.ver_detalle_oferta.as_view(), name='ver_detalle_oferta'),
    path('editar_oferta/<int:oferta_id>/', views_editar.editar_oferta, name='editar_oferta'),
]