from django.urls import path
from .views import ver_ofertas

urlpatterns = [
    path('ver_ofertas/<int:id>/', ver_ofertas, name='ver_ofertas'),
    # otras rutas
]
