from django.utils import timezone
from Aplicaciones.Modelos.models import Publicidad

def publicidad_context_processor(request):
    hoy = timezone.now().date()
    publicidad = Publicidad.objects.filter(fecha=hoy).first()
    return {'publicidad': publicidad}
