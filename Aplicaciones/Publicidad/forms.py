from django import forms
from django.core.exceptions import ValidationError
from MDI.widgets import MultipleFileInput 
from .models import Publicidad
from datetime import date, timedelta  # Importa date y timedelta desde el módulo datetime para manejar fechas

class PublicidadForm(forms.ModelForm):

    class Meta:
        model = Publicidad
        fields = ('fecha','cliente', 'foto_central', 'foto_lateral',)
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def clean_fecha(self):
        fecha_aux = self.cleaned_data.get('fecha')
        if Publicidad.objects.filter(fecha=fecha_aux).exists():
            raise ValidationError("La fecha ingresada ya esta ocupada")
        return fecha_aux
    
    def clean(self):
        cleaned_data = super().clean()
        foto_central = cleaned_data.get('foto_central')
        foto_lateral = cleaned_data.get('foto_lateral')

        if not foto_central:
            raise forms.ValidationError("Debe subir una foto para el banner central.")
        
        if not foto_lateral:
            raise forms.ValidationError("Debe subir una foto para el banner lateral.")

        return cleaned_data


    
