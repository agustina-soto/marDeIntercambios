from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    template_name = 'multiple_file_input.html'
    initial_text = 'Seleccionar archivos'
    input_text = ''
    clear_checkbox_label = 'Eliminar'
