from django import forms
from django.utils import timezone
from MDI.widgets import MultipleFileInput
from .models import Publicacion, FotoPublicacion
from Aplicaciones.AdministracionPublicaciones.choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator


class PublicacionForm(forms.ModelForm):
    # Declaración de campos adicionales que no están definidos en el modelo
    titulo = forms.CharField(label='Título', required=False)
    tipo_embarcacion = forms.ChoiceField(label='Tipo de Embarcación', choices=[('', 'Seleccione un tipo de embarcación')] + TIPOS_EMBARCACION, required=False)
    anio = forms.IntegerField(label='Año', min_value=1900, max_value=timezone.now().year, required=False)
    precio_minimo = forms.DecimalField(label='Precio mínimo permitido', validators=[MinValueValidator(0)], required=False)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'precio_minimo', 'tipo_embarcacion', 'anio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asigna clases y placeholders a los campos del formulario
        self.fields['titulo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el título'})
        self.fields['precio_minimo'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio mínimo'})
        self.fields['anio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el año'})

    # Métodos de validación personalizados para cada campo
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
        if not anio or (anio < 1900 or anio > timezone.now().year):
            raise forms.ValidationError('El año debe estar entre 1900 y el año actual.')
        return anio

    def clean_tipo_embarcacion(self):
        tipo_embarcacion = self.cleaned_data.get('tipo_embarcacion')
        if not tipo_embarcacion:
            raise forms.ValidationError('Por favor, complete este campo.')
        return tipo_embarcacion
    
class FotoPublicacionForm(forms.ModelForm):
   
    foto = forms.ImageField(
        widget = MultipleFileInput(),
        required = False #anulo la verificación por defecto del formulario para control manual
    )

    class Meta:
        model = FotoPublicacion
        fields = ['foto']

    def clean_foto(self):
        cleaned_data = super().clean()
        fotos = cleaned_data.get('foto')
        if not fotos:
            raise forms.ValidationError('Debes proporcionar al menos una foto.')
        return cleaned_data