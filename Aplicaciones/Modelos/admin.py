from django.contrib import admin
from .models import Publicidad

# gestiona las publicidades desde la interfaz de administración de Django
@admin.register(Publicidad)
class PublicidadAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_inicio', 'fecha_fin')
