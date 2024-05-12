from django.apps import AppConfig


class IniciarsesionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Autenticacion.IniciarSesion' # tiene que ir 'Aplicaciones.Autenticacion' porque mi app esta adentro de esa carpeta