from django import forms
from Aplicaciones.GestionUsuarios.RegistrarUsuario.models import Usuario
from django.core.exceptions import ValidationError
from django.contrib import messages

class LoginForm(forms.Form):
    username = forms.CharField(label='Correo electronico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

#VERIFICACIONES
    def clean_username(self):
        unUsuario = self.cleaned_data.get('username', '')
        if not Usuario.objects.filter(username=unUsuario).exists():
            raise ValidationError("Usuario o contraseña no validos. Por favor, intenta de nuevo")
        return unUsuario