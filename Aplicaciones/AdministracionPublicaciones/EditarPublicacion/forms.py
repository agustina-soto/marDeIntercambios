from django import forms

from .models import Publicacion, FotoPublicacion
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION

from MDI.widgets import MultipleFileInput

from django.core.validators import MinValueValidator, MaxValueValidator


class EditarPublicacionForm(forms.ModelForm):
    tipo_embarcacion = forms.ChoiceField(choices=TIPOS_EMBARCACION)
    anio = forms.IntegerField(validators=[MinValueValidator(1900)])
    precio_minimo = forms.DecimalField(validators=[MinValueValidator(0)])
    
    class Meta:
        model = Publicacion
        fields = ['titulo', 'precio_minimo', 'tipo_embarcacion', 'anio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formulario con los valores actuales de la publicación
        if self.instance:
            self.initial['tipo_embarcacion'] = self.instance.tipo_embarcacion
            self.initial['anio'] = self.instance.anio
            self.fields['precio_minimo'].validators.append(MinValueValidator(0))


class EditarFotoPublicacionForm(forms.ModelForm):
    class Meta:
        model = FotoPublicacion
        fields = ['foto']
        widgets = {
            'foto': MultipleFileInput(),
        }
