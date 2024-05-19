from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class MultipleFileInput(ClearableFileInput):
    template_name = 'multiple_file_input.html'
    initial_text = _('Seleccionar archivos')
    input_text = _('')
    clear_checkbox_label = _('Eliminar')
