#PARA MOSTRAR EL MENSAJE DE ADVERTENCIA DE MENSAJES EN TODAS LAS PLANTILLAS

from Aplicaciones.Modelos.models import Room

def unread_messages_processor(request):
    if request.user.is_authenticated:
        unread_count = Room.objects.filter(roomuser__user=request.user, roomuser__unread_messages=True).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}
