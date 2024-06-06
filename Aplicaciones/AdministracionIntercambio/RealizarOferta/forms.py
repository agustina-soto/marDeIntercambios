from django import forms
from .models import Oferta, FotoOferta

from Aplicaciones.AdministracionPublicaciones.RealizarPublicacion.models import Publicacion
from MDI.widgets import MultipleFileInput

class OfertaForm (forms.ModelForm):
    precio_estimado = forms.DecimalField(label='Precio estimado', required=False) 
    descripcion = forms.CharField(label='Descripción', required=False)

    class Meta:
        model = Oferta
        fields = ['precio_estimado', 'descripcion']

    def __init__(self, *args, **kwargs):
       self.publicacion = kwargs.pop('publicacion', None)  # Extraemos el objeto publicacion del kwargs
       super().__init__(*args, **kwargs)
       # método inicializador de una clase en Python y se ejecuta cuando se crea una nueva instancia de esa clase
       #se utiliza para personalizar el comportamiento del formulario al momento de su creación
       self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese la descripción'})
       self.fields['precio_estimado'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio estimado'})

    #funciones de validacion personalizados

    def clean(self):
        cleaned_data = super().clean()
        self.clean_publicacion()
        return cleaned_data
    
    def clean_publicacion (self):
        publicacion = self.publicacion
        if publicacion.estado != 'pendiente':
            raise forms.ValidationError('La publicación no puede recibir ofertas por el momento porque esta a la espera de validación.') 
        return publicacion
    
    def clean_descripcion (self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion:
            raise forms.ValidationError('Por favor, complete este campo.')
        return descripcion

    def clean_precio_estimado(self):
        precio_estimado = self.cleaned_data.get('precio_estimado')
        publicacion = self.publicacion

        if publicacion is None:
            raise forms.ValidationError('La publiaccion no es valida')

        if precio_estimado is not None:
            if precio_estimado < publicacion.precio_minimo:
                raise forms.ValidationError('El precio estimado debe ser mayor o igual que el precio mínimo de la publicación.') 
        else:
            raise forms.ValidationError('Por favor, complete este campo')       
        
        return precio_estimado #si no hay error con los datos devuelve el diccionario cleaned_data que contiene los datos validados del formulario.
    
class FotoOfertaForm (forms.ModelForm): #buscar la posibilidad de unificar esta clase con la de publicacion sino es mucho repetir cod
    foto = forms.ImageField( #campo que permite subir imagenes 
        widget= MultipleFileInput(), #permite subir mas de una imagen a la vez
        required=False,
    )

    class Meta:
        model = FotoOferta
        fields = ['foto']

    """def clean_foto(self): #copie y pegue de agus 
        cleaned_data = super().clean()
        fotos = cleaned_data.get('foto')
        if not fotos:
            raise forms.ValidationError('Debes proporcionar al menos una foto.')
        return cleaned_data""" #no es obligatorio que se proporcione una foto


