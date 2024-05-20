from django.utils import timezone
from django import forms

from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from .models import Publicacion, FotoPublicacion
from MDI.widgets import MultipleFileInput
from django.core.validators import MinValueValidator


class EditarPublicacionForm(forms.ModelForm):
    titulo = forms.CharField(label='Título')
    tipo_embarcacion = forms.ChoiceField(label='Tipo de Embarcación', choices=[('', 'Seleccione un tipo de embarcación')] + TIPOS_EMBARCACION)    
    anio = forms.IntegerField(label='Año', min_value=1900, max_value=timezone.now().year)
    precio_minimo = forms.DecimalField(label='Precio mínimo permitido', validators=[MinValueValidator(0)])
    tipo_embarcacion = forms.ChoiceField(label='Tipo de Embarcación', choices=[('', 'Seleccione un tipo de embarcación')] + TIPOS_EMBARCACION) 

    class Meta:
        model = Publicacion
        fields = ['titulo', 'precio_minimo', 'tipo_embarcacion', 'anio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formulario con los valores actuales de la publicación
        if self.instance:
            self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el título'})
            self.fields['precio_minimo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio minimo'})
            self.fields['anio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el año'})
        
        # Asigna el valor inicial al campo tipo_embarcacion obteniendo el valor actual del tipo de embarcación de la instancia
        self.initial['tipo_embarcacion'] = self.instance.tipo_embarcacion  # NO LO HACE BIEN 

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            raise forms.ValidationError('Por favor, complete este campo.')
        return titulo

    def clean_precio_minimo(self):
        precio_minimo = self.cleaned_data.get('precio_minimo')
        if not precio_minimo:
            raise forms.ValidationError('Por favor, complete este campo.')
        return precio_minimo

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        if anio is not None and (anio < 1900 or anio > timezone.now().year):
            raise forms.ValidationError('El año debe estar entre 1900 y el año actual.')
        return anio
    
    def clean_tipo_embarcacion(self):
        tipo_embarcacion = self.cleaned_data.get('tipo_embarcacion')
        if not tipo_embarcacion:
            raise forms.ValidationError('Por favor, complete este campo.')
        return tipo_embarcacion


class EditarFotoPublicacionForm(forms.ModelForm):
    class Meta:
        model = FotoPublicacion
        fields = ['foto']
        widgets = {
            'foto': MultipleFileInput(),
        }
