from django import forms
from .models import Publicacion
from .choices import TIPOS_EMBARCACION
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone

class PublicacionForm(forms.ModelForm):
    tipo_embarcacion = forms.ChoiceField(choices=TIPOS_EMBARCACION)
    anio = forms.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)])
    
    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if len(foto) > 3:
            raise forms.ValidationError('Solo se permiten hasta 3 imágenes por publicación.')
        return foto

    class Meta:
        model = Publicacion
        fields = ['titulo', 'precio_minimo', 'tipo_embarcacion', 'anio', 'foto']
