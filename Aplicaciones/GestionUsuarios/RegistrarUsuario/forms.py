import re
import datetime
from django import forms
from datetime import date
from .models import Usuario
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):

    username = forms.CharField(label='Correo Electronico', required=False)

    dni = forms.IntegerField(label= 'DNI', required=False,
        widget=forms.NumberInput(attrs={
            'maxlength': 8,
            'oninput': "this.value=this.value.slice(0,this.maxLength)"})) #Aseguro que se coloquen hasta 8 dígitos.
    
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '1910-01-01',
            'max': date.today().strftime('%Y-%m-%d')})) #limito fechas de nacimiento entre a rango 1910-añoActual
    
    password1 = forms.CharField(label='Contraseña', required=False,
        widget=forms.PasswordInput()) #Escondo password
    
    password2 = forms.CharField(label='Confirmar Contraseña', required=False,
        widget=forms.PasswordInput())
    

    class Meta:
        model = Usuario
        fields = ('username', 'dni', 'fecha_nacimiento', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['dni'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

#VERIFICACIONES

    #Username
    def clean_username(self):
        unUsuario = self.cleaned_data.get('username','')
        if not unUsuario or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', unUsuario):
            raise ValidationError("Por favor, introduce un correo electrónico válido.")
        if Usuario.objects.filter(username=unUsuario).exists():
            raise ValidationError("El nombre de usuario ingresado ya se encuentra registrado")
        return unUsuario
    
    #Documento
    def clean_dni(self):
        unDni = self.cleaned_data.get('dni', '')
        if not unDni or (unDni < 10000000):
            raise ValidationError("Por favor, introduzca un dni de 8 dígitos válido")
        if Usuario.objects.filter(dni=unDni).exists():
            raise ValidationError("El DNI ingresado ya se encuentra registrado")
        return unDni
    
    #Fecha De Nacimiento
    def clean_fecha_nacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fecha_nacimiento', None)
        hoy = datetime.date.today()
        edad = relativedelta(hoy, fechaNacimiento).years
        if not fechaNacimiento or edad < 18:
            raise ValidationError("Para registrarse debe ser mayor a 18 años") #Hay que testear para casos especiales
        return fechaNacimiento
    
    #Passwords
    def clean_password1(self):
        pass1 = self.cleaned_data.get('password1','')
        if not pass1 or (len(pass1) < 8 ):
            raise ValidationError("La contraseña debe tener más de 7 dígitos")
        return pass1

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1','')
        pass2 = self.cleaned_data.get('password2', '')
        if (pass1 != pass2):
            raise ValidationError("Las contraseñas no coinciden") #NO ESTÁ EN LA H.U DEL PIVOTAL, HABRÍA QUE PONERLO? 
        return pass2
    
class RegistroFormAdministrador(forms.ModelForm):

    username = forms.CharField(label='Correo Electronico', required=False)

    dni = forms.IntegerField(label= 'DNI', required=False,
        widget=forms.NumberInput(attrs={
            'maxlength': 8,
            'oninput': "this.value=this.value.slice(0,this.maxLength)"})) #Aseguro que se coloquen hasta 8 dígitos.
    
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '1910-01-01',
            'max': date.today().strftime('%Y-%m-%d')})) #limito fechas de nacimiento entre a rango 1910-añoActual

    class Meta:
        model = Usuario
        fields = ('username', 'dni', 'fecha_nacimiento')

#VERIFICACIONES

    #Username
    def clean_username(self):
        unUsuario = self.cleaned_data.get('username','')
        if not unUsuario or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', unUsuario):
            raise ValidationError("Por favor, introduce un correo electrónico válido.")
        if Usuario.objects.filter(username=unUsuario).exists():
            raise ValidationError("El nombre de usuario ingresado ya se encuentra registrado")
        return unUsuario
    
    #Documento
    def clean_dni(self):
        unDni = self.cleaned_data.get('dni', '')
        if not unDni or (unDni < 10000000):
            raise ValidationError("Por favor, introduzca un dni de 8 dígitos válido")
        if Usuario.objects.filter(dni=unDni).exists():
            raise ValidationError("El DNI ingresado ya se encuentra registrado")
        return unDni
    
    #Fecha De Nacimiento
    def clean_fecha_nacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fecha_nacimiento', None)
        hoy = datetime.date.today()
        edad = relativedelta(hoy, fechaNacimiento).years
        if not fechaNacimiento or edad < 18:
            raise ValidationError("Para registrarse debe ser mayor a 18 años") #Hay que testear para casos especiales
        return fechaNacimiento