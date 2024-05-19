from django import forms
from django.utils import timezone
from MDI.widgets import MultipleFileInput
from .models import Publicacion, FotoPublicacion
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator


class PublicacionForm(forms.ModelForm):
    tipo_embarcacion = forms.ChoiceField(choices=TIPOS_EMBARCACION)
    anio = forms.IntegerField(validators=[MinValueValidator(1900)])
    precio_minimo = forms.DecimalField(validators=[MinValueValidator(0)])


    class Meta:
        model = Publicacion
        fields = ['titulo', 'precio_minimo', 'tipo_embarcacion', 'anio']

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        if anio is not None and (anio < 1900 or anio > timezone.now().year):
            raise forms.ValidationError('El año debe estar entre 1900 y el año actual.')
        return anio


class FotoPublicacionForm(forms.ModelForm):
    class Meta:
        model = FotoPublicacion
        fields = ['foto']
        widgets = {
            'foto': MultipleFileInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fotos = cleaned_data.get('foto')
        if not fotos:
            raise forms.ValidationError('Debes proporcionar al menos una foto.') #nunca entra aca...!!
        return cleaned_data
    
