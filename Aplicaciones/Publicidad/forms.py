from django import forms
from django.core.exceptions import ValidationError
from MDI.widgets import MultipleFileInput 
from .models import Publicidad
from datetime import date, timedelta  # Importa date y timedelta desde el módulo datetime para manejar fechas
from django.utils import timezone

class PublicidadForm(forms.ModelForm):
    cliente = forms.CharField(label='Cliente', required=False)

    fecha = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'datepicker form-control',
        'id': 'fecha',
        'name': 'fecha',
        'min': date.today().strftime('%Y-%m-%d')  # Establece el mínimo como la fecha actual
    }))
    
    class Meta:

        model = Publicidad
        fields = ('fecha','cliente', 'foto_central', 'foto_lateral')
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs.update({'class': 'form-control'})
        self.fields['foto_central'].widget.attrs.update({'class': 'form-control'})
        self.fields['foto_lateral'].widget.attrs.update({'class': 'form-control'})

    """def clean_fecha(self):
        fecha_aux = self.cleaned_data.get('fecha')
        if not fecha_aux:
            self.add_error('fecha', "Por favor, ingrese una fecha")
        else: 
            if Publicidad.objects.filter(fecha=fecha_aux).exists():
                self.add_error('fecha', "La fecha ingresada ya está ocupada")
                #raise ValidationError("La fecha ingresada ya esta ocupada")
        return fecha_aux"""
    
    def clean_fecha(self):
        fecha_aux = self.cleaned_data.get('fecha')
        if not fecha_aux:
            self.add_error('fecha', "Por favor, ingrese una fecha")
        else: 
            # Excluir la instancia actual en la validación
            if Publicidad.objects.filter(fecha=fecha_aux).exclude(id=self.instance.id).exists():
                self.add_error('fecha', "La fecha ingresada ya está ocupada")
                #raise ValidationError("La fecha ingresada ya esta ocupada")
        return fecha_aux
    
    def clean(self):
        cleaned_data = super().clean()
        foto_central = cleaned_data.get('foto_central')
        foto_lateral = cleaned_data.get('foto_lateral')

        if not foto_central:
            self.add_error('foto_central', "Debe subir una foto para el banner central")
            #raise forms.ValidationError("Debe subir una foto para el banner central.")
        
        if not foto_lateral:
            self.add_error('foto_lateral', "Debe subir una foto para el banner lateral.")
            #raise forms.ValidationError("Debe subir una foto para el banner lateral.")

        return cleaned_data


    
