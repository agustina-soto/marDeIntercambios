from django import forms
from django.core.exceptions import ValidationError
from Aplicaciones.GestionUsuarios.RegistrarUsuario.models import Usuario

class LoginForm(forms.Form):
    username = forms.CharField(label='Correo electronico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

#VERIFICACIONES
    def clean_username(self):
        unUsuario = self.cleaned_data.get('username', '')
        if not Usuario.objects.filter(username=unUsuario).exists():
            raise ValidationError("Error, no se encontró usuario en BD") 
        return unUsuario