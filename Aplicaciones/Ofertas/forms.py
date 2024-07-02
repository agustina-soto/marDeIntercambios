from datetime import date
import datetime
import re
from dateutil.relativedelta import relativedelta
from django import forms
from Aplicaciones.Modelos.models import Oferta, FotoOferta, Usuario
from Aplicaciones.Modelos.models import Publicacion
from MDI.widgets import MultipleFileInput

"""class OfertaForm (forms.ModelForm):
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
        if publicacion.estado != 'pendiente': #deberia de ser igual a pendiente pero para probar lo deje en != 
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
        fields = ['foto']"""

class OfertaForm(forms.ModelForm):
    precio_estimado = forms.DecimalField(label='Precio estimado', required=False) 
    descripcion = forms.CharField(label='Descripción', required=False)
    #Agrego campos para usuario
    visitante = forms.CharField(label='Correo Electronico', required=False)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=False, 
        widget=forms.DateInput(attrs={
            'type': 'date',
            'min': '1910-01-01',
            'max': date.today().strftime('%Y-%m-%d')})) #limito fechas de nacimiento entre a rango 1910-añoActual  
    dni = forms.IntegerField(label='DNI', required=False,
        widget=forms.NumberInput(attrs={
            'maxlength': 8,
            'oninput': "this.value=this.value.slice(0,this.maxLength)"})) #Aseguro que se coloquen hasta 8 dígitos.
    
    class Meta:
        model = Oferta
        fields = ['precio_estimado', 'descripcion', 'visitante', 'fecha_nacimiento', 'dni']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Extraemos el objeto request del kwargs
        self.publicacion = kwargs.pop('publicacion', None)  # Extraemos el objeto publicacion del kwargs
        super().__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese la descripción'})
        self.fields['precio_estimado'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el precio estimado'})
        self.fields['visitante'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el correo electronico'})
        self.fields['dni'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese el dni'})
        self.fields['fecha_nacimiento'].widget.attrs.update({'class': 'form-control'})

    #Controlo usuario registrado
    def clean(self):
        cleaned_data = super().clean()
        self.clean_publicacion()
        #Si es usuario autenticado, saco las restricciones para evitar que me tire errores, ya que oculté los campos
        if self.request and self.request.user.is_authenticated:
            # Si el usuario está autenticado, eliminamos errores de los campos no necesarios
            self.cleaned_data['visitante'] = self.request.user.username  # Asumimos que el correo está en user.email
            self.cleaned_data['dni'] = self.request.user.dni  # Asumimos que el perfil tiene dni
            self.cleaned_data['fecha_nacimiento'] = self.request.user.fecha_nacimiento  # Asumimos que el perfil tiene fecha de nacimiento
            self._errors.pop('visitante', None)
            self._errors.pop('dni', None)
            self._errors.pop('fecha_nacimiento', None)
        
        return cleaned_data

    def clean_publicacion(self):
        publicacion = self.publicacion
        if publicacion and publicacion.estado != 'pendiente':  # Verificamos el estado de la publicación
            raise forms.ValidationError('La publicación no puede recibir ofertas por el momento porque está a la espera de validación.') 
        return publicacion
    
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion:
            raise forms.ValidationError('Por favor, complete este campo.')
        return descripcion

    def clean_precio_estimado(self):
        precio_estimado = self.cleaned_data.get('precio_estimado')
        publicacion = self.publicacion

        if not publicacion:
            raise forms.ValidationError('La publicación no es válida')

        if precio_estimado is not None:
            if precio_estimado < publicacion.precio_minimo:
                raise forms.ValidationError('El precio estimado debe ser mayor o igual que el precio mínimo de la publicación.') 
        else:
            raise forms.ValidationError('Por favor, complete este campo')       
        
        return precio_estimado
    
    def clean_dni(self):
        unDni = self.cleaned_data.get('dni', '')
        if not unDni or (unDni < 10000000):
            raise forms.ValidationError("Por favor, introduzca un DNI de 8 dígitos válido")
        if Usuario.objects.filter(dni=unDni).exists():
            raise forms.ValidationError("El DNI ingresado ya se encuentra registrado")
        return unDni
    
    def clean_fecha_nacimiento(self):
        fechaNacimiento = self.cleaned_data.get('fecha_nacimiento', None)
        hoy = datetime.date.today()
        edad = relativedelta(hoy, fechaNacimiento).years
        if not fechaNacimiento or edad < 18:
            raise forms.ValidationError("Para registrarse debe ser mayor a 18 años")
        return fechaNacimiento
    
    def clean_visitante(self):
        unUsuario = self.cleaned_data.get('visitante', '')
        if not unUsuario or not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', unUsuario):
            raise forms.ValidationError("Por favor, introduce un correo electrónico válido.")
        return unUsuario

class FotoOfertaForm(forms.ModelForm):
    foto = forms.ImageField(
        widget=MultipleFileInput(),
        required=False,
    )

    class Meta:
        model = FotoOferta
        fields = ['foto']

#------------------------------------------ editar oferta -------------------------------

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
