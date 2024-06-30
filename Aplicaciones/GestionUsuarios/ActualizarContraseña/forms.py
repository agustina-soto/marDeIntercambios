from django import forms
from django.core.exceptions import ValidationError

class ActualizarPasswordForm(forms.Form):
    oldPassword = forms.CharField(label='Contraseña actual', required=False,
        widget=forms.PasswordInput())
    newPassword = forms.CharField(label='Contraseña nueva', required=False,
        widget=forms.PasswordInput()) 
    newPasswordRepeat = forms.CharField(label='Confirmación de contraseña', required=False,
        widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs) 
        self.fields['oldPassword'].widget.attrs.update({'class': 'form-control'})
        self.fields['newPassword'].widget.attrs.update({'class': 'form-control'})
        self.fields['newPasswordRepeat'].widget.attrs.update({'class': 'form-control'})

    #Passwords

    def clean(self):
        cleaned_data = super().clean()
        oldPass = self.cleaned_data.get('oldPassword')
        newPass = self.cleaned_data.get('newPassword')
        newPassRepeat = self.cleaned_data.get('newPasswordRepeat')

        if not oldPass or not self.user.check_password(oldPass):
            self.add_error('oldPassword', "La contraseña de usuario es incorrecta")
            return cleaned_data
        if not newPass or (len(newPass) < 8):
            self.add_error('newPassword', "La contraseña nueva debe tener 8 o más caracteres.")
        if (newPass != newPassRepeat):
            self.add_error('newPassword', "La contraseña nueva no coincide. Vuelve a ingresarla")
        if (self.user and self.user.check_password(newPass)):
            self.add_error('newPassword', "La contraseña nueva es igual a la actual")
        return cleaned_data
    