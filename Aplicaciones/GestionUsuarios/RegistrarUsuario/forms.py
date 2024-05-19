import re
import datetime
from django import forms
from .models import Usuario
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    username = forms.CharField(label='Correo Electronico')
    dni = forms.IntegerField(label= 'DNI', required=True, min_value=10000000, max_value=99999999)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput())

    class Meta:
        model = Usuario
        fields = ('username', 'dni', 'fecha_nacimiento', 'password1', 'password2')

#VERIFICACIONES

    #Username
    def clean_username(self):
        unUsuario = self.cleaned_data.get('username','')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', unUsuario):
            raise ValidationError("Por favor, introduce un correo electrónico válido.")
        if Usuario.objects.filter(username=unUsuario).exists():
            raise ValidationError("El nombre de usuario ingresado ya se encuentra registrado")
        return unUsuario
    
    #Documento
    def clean_dni(self):
        unDni = self.cleaned_data.get('dni', '')
        if Usuario.objects.filter(dni=unDni).exists():
            raise ValidationError("El DNI ingresado ya se encuentra registrado")
        return unDni
    
    #Fecha De Nacimiento
    def clean_fecha_nacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fecha_nacimiento', None)
        hoy = datetime.date.today()
        edad = relativedelta(hoy, fechaNacimiento).years
        if edad < 18:
            raise ValidationError("Para registrarse debe ser mayor a 18 años") #Hay que testear para casos especiales
        return fechaNacimiento
    
    #passwords
    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1','')
        pass2 = self.cleaned_data.get('password2', '')
        if (pass1 != pass2):
            raise ValidationError("Las contraseñas no coinciden") #NO ESTÁ EN LA H.U DEL PIVOTAL, HABRÍA QUE PONERLO? 
        return pass2