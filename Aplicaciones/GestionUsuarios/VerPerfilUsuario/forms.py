from datetime import date
from django import forms
from Aplicaciones.Modelos.models import Usuario
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model


# FORMULARIO PARA EDITAR EL PERFIL DE UN USUARIO
class EditarPerfilForm(forms.ModelForm):
    # Defino los campos a editar, nombre y apellido no se puede porque n existe relacion entre usuario y persona y esos dos campos son de persona
    # nombre = forms.CharField(label='Nombre', required=False)
    # apellido = forms.CharField(label='Apellido', required=False)
    dni = forms.IntegerField(label='DNI')
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento')


    class Meta:
        model = Usuario
        fields = ['dni', 'fecha_nacimiento'] # 'nombre', 'apellido',
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        # self.fields['apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['dni'].widget.attrs.update({'class': 'form-control'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control'})

        
    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        if not fecha_nacimiento:
            raise forms.ValidationError('Este campo es obligatorio.')

        # Validacion de edad minima (mayor o igual a 18 años)
        edad_minima = date.today().year - fecha_nacimiento.year - ((date.today().month, date.today().day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        if edad_minima < 18:
            raise forms.ValidationError('Debe ser mayor de edad para registrarse.')

        return fecha_nacimiento

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            raise forms.ValidationError('Este campo es obligatorio.')

        # Validacion de DNI unico
        if self.instance.dni != dni and Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError('El DNI ingresado ya está registrado.')

        return dni


# FORMULARIO PARA ACTUALIZAR LA CONTRASEÑA
User = get_user_model()

class ActualizarPassForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres.')

        try:
            password_validation.validate_password(password1, self.user)
            print('Contraseña validada')
        except forms.ValidationError as error:
            self.add_error('new_password1', error)

        return password1

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user