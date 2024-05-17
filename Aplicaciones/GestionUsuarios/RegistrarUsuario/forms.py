import re #PARA QUE EL EMAIL Y EL DNI CUMPLA CON UNA CADENA PARTICULAR
from django import forms
from django.core.exceptions import ValidationError
from .models import UsuarioRegistrado
from datetime import date
from dateutil.relativedelta import relativedelta # pip install python-dateutil(para calcular la fecha como en java)

#comienzo a crear mi formulario personalizado heredando el formulario por defecto que tiene Django(ModelForm)
class UsuarioRegistradoForm(forms.ModelForm):

    email = forms.CharField(label='Correo electrónico', required=False) #Saco los required del imput email, no me quedó otra que colocarlo aparte
    contraseña2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(), required=False) #creo un campo contraseña2 para la confirmación

    class Meta:
        model = UsuarioRegistrado
        fields = ['email', 'contraseña', 'dni', 'fecha_nacimiento'] #Creo el formulario con los campos que necesito(obvio que el modelo tiene que tener los campos)
        widgets = {
            'contraseña': forms.PasswordInput(),  # Para ocultar la contraseña
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),  # Para usar un widget de fecha
        }
        labels = {
            #Para usarlos en el html
            'email': 'Correo electrónico',
            'contraseña': 'Contraseña',
            'dni': 'DNI',
            'fecha_nacimiento': 'Fecha de nacimiento',
        }

    #VALIDACIONES DE CADA CAMPO
    def clean_email(self):
        auxemail = self.cleaned_data.get('email', '')
        if not auxemail:
            raise ValidationError("Por favor, introduce un correo electrónico válido")
        if UsuarioRegistrado.objects.filter(email=auxemail).exists():
            raise ValidationError("El nombre de usuario ingresado ya se encuentra registrado")
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', auxemail):
            raise ValidationError("Por favor, introduce un correo electrónico válido.")
        return auxemail

    def clean_dni(self):
        auxdni = self.cleaned_data.get('dni', '')
        if not auxdni:
            raise ValidationError("El DNI es requerido.")
        if UsuarioRegistrado.objects.filter(dni=auxdni).exists():
            raise ValidationError("El DNI ingresado ya se encuentra registrado")
        if not re.match(r'^[0-9]{8}$', auxdni):
            raise ValidationError("El formato del DNI no es válido. Por favor, introduce un DNI con 8 números.")
        return auxdni

    def clean_contraseña(self):
        contraseña = self.cleaned_data.get('contraseña')
        contraseña2 = self.cleaned_data.get('contraseña2')
        if not contraseña:
            raise ValidationError("La contraseña es requerida")
        if len(contraseña) < 8:
            raise ValidationError("La contraseña debe tener más de 7 dígitos")
        return contraseña

    def clean_contraseña2(self):
        contraseña = self.cleaned_data.get('contraseña')
        contraseña2 = self.cleaned_data.get('contraseña2')

        if not contraseña2:
            raise ValidationError("La confirmación de la contraseña es requerida")
        if contraseña != contraseña2:
            raise ValidationError("Las contraseñas no coinciden")
        return contraseña2

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento', None)
        if not fecha_nacimiento:
            raise ValidationError("La fecha de nacimiento es requerida.")
        today = date.today()
        age = relativedelta(today, fecha_nacimiento).years
        #age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if age < 18:
            raise ValidationError("Para registrarse debe ser mayor a 18 años")
        return fecha_nacimiento

    # Deshabilito las demás validaciones que vienen por defecto, para poner las propias
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False  # Deshabilita la validación de campo requerido
 