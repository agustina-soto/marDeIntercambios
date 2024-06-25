"""
Django settings for MDI project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-efg^=gz(uisc9p4y#&r#=u0jg0&@*ks+3k5nkp^soyc(%vl2&v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', 
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "daphne", #Para el chat pip install daphne
    'django.contrib.staticfiles',
    'Aplicaciones.Modelos',
    'Aplicaciones.Autenticacion.IniciarSesion',
    'Aplicaciones.Autenticacion.CerrarSesion',
    'Aplicaciones.GestionUsuarios.RegistrarUsuario',
    'Aplicaciones.GestionUsuarios.VerPerfilUsuario',
    'Aplicaciones.GestionUsuarios.ActualizarContraseña',
    'Aplicaciones.AdministracionPublicaciones.RealizarPublicacion',
    'Aplicaciones.AdministracionPublicaciones.EditarPublicacion',
    'Aplicaciones.AdministracionPublicaciones.BorrarPublicacion',
    'Aplicaciones.VisualizacionPublicaciones.BuscarPublicacion',
    'Aplicaciones.VisualizacionPublicaciones.VerDetallePublicacion',
    'Aplicaciones.VisualizacionPublicaciones.Comparacion',
    'Aplicaciones.VisualizacionPublicaciones.Favoritos',
    'Aplicaciones.AdministracionIntercambio.RealizarOferta',
    'Aplicaciones.AdministracionIntercambio.EditarOferta',
    'Aplicaciones.ComunicacionEntreUsuarios.SalaDeChat',
    'Aplicaciones.ComunicacionEntreUsuarios.BandejaDeMensajes',
    'Aplicaciones.Ofertas',
    'channels', #Para el chat pip install channels
    "channels_redis", #Para el chat pip install channels_redis
    'Aplicaciones.Notificaciones.Notificacion'
]

#'anymail', #Correo pip install django-anymail (Lo dejo acá, lo más probable es que lo volemos luego de la demo)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MDI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 # Añado procesador de contexto personalizado
                'Aplicaciones.ComunicacionEntreUsuarios.BandejaDeMensajes.context_processors.unread_messages_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'MDI.wsgi.application'

# para el chat
ASGI_APPLICATION = 'MDI.asgi.application'

# Configuración del canal layer (puedes usar Redis para producción)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #Luck: Quito algunas validaciones
    #{
    #    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    #},
    #{
    #    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #},
  
    #{
    #    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #},
    #{
    #    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    #},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/archivos-estaticos/'

STATIC_ROOT = '/archivos-estaticos/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'archivos-estaticos'), # Los archivos static se buscan aca
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Especifica el modelo de usuario personalizado
AUTH_USER_MODEL = 'Modelos.Usuario'

LOGIN_URL = 'login' # Esto le dice a Django que redirija a la URL llamada login cuando un usuario no autenticado intente acceder a una vista protegida

#PARA EL ENVIO DE CORREO ELECTRONICO (CON CORREO APARTE, SOLO FUNCIONA PARA 10 EMAILS Y DESPUES TE SALTA ERROR DE SPAM)
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp-mail.outlook.com'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'Glam.Tech@hotmail.com'
#EMAIL_HOST_PASSWORD = 'GlamTech2024'

EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

ANYMAIL = {
    "MAILGUN_API_KEY": "84fa9a60811232f31aa3f09350ff7e7a-51356527-8336bd6b",
    "MAILGUN_SENDER_DOMAIN": "sandboxbd2e9d473ef2468aa3aa326aa72d36fd.mailgun.org",  # Debes verificar y usar tu propio dominio
}

DEFAULT_FROM_EMAIL = "Glam.Tech@sandboxbd2e9d473ef2468aa3aa326aa72d36fd.mailgun.org"  # Asegúrate de usar el mismo dominio

MESSAGE_TAGS = {
        messages.ERROR: 'danger',
}