from django import forms
from Aplicaciones.AdministracionIntercambio.RealizarOferta.models import Oferta, FotoOferta
from MDI.widgets import MultipleFileInput

class EditarOfertaForm (forms.ModelForm):
    precio_estimado = forms.DecimalField(label='Precio estimado', required=False) 
    descripcion = forms.CharField(label='Descripción', required=False)
    estado = forms.CharField(max_length=10, required=False) 

    class Meta:
        model = Oferta
        fields = ['precio_estimado', 'descripcion', 'estado']

    def __init__(self, *args, **kwargs):
       self.publicacion = kwargs.pop('publicacion', None)  # Extraemos el objeto publicacion del kwargs
       super().__init__(*args, **kwargs)
       # método inicializador de una clase en Python y se ejecuta cuando se crea una nueva instancia de esa clase
       #se utiliza para personalizar el comportamiento del formulario al momento de su creación
       if self.instance:
            self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese la descripción'})
            self.fields['precio_estimado'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio estimado'})

    #funciones de validacion personalizados

    def clean(self):
        cleaned_data = super().clean()
        self.clean_estado()
        return cleaned_data
    
    #si la oferta ya fue aceptada no se puede editar
    def clean_estado (self):
        estado = self.cleaned_data.get('estado')
        if estado == 'aceptada':
            raise forms.ValidationError('La oferta ya fue aceptada por el dueño de la publicación y no se puede modificar.') 
        return estado
    
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


class EditarFotoOfertaForm (forms.ModelForm):
    class Meta:
        model = FotoOferta
        fields = ['foto']
        widgets = {
            'foto': MultipleFileInput(),
        }