from django.urls import path

from . import views


urlpatterns = [
    path("programar_publicidad/", views.programar_publicidad, name='programar_publicidad'),
    path('mostrar_publicidad_central/', views.mostrar_publicidad_central, name='mostrar_publicidad'),
    path('mostrar_publicidad_lateral/', views.mostrar_publicidad_lateral, name='mostrar_publicidad_lateral'),
    path('listar_publicidades/', views.listar_publicidades, name='listar_publicidades'),
    path('eliminar_publicidad/<int:pk>/', views.eliminar_publicidad, name='eliminar_publicidad'),
    path('editar/<int:id>/', views.editar_publicidad, name='editar_publicidad'),
    path('previsualizar/<int:pk>/', views.previsualizar_publicidad, name='previsualizar_publicidad'),
]