from django.utils import timezone
from Aplicaciones.Modelos.models import Notificacion

class NotificationManager:
    def __init__(self):
        pass

    def crear_notificacion(self, user, message, tipo):
        """
        Crea una nueva notificación y la guarda en la base de datos.
        
        :param user: Usuario que recibirá la notificación.
        :param message: Mensaje de la notificación.
        :param notification_type: Tipo de notificación.
        :return: La notificación creada.
        """
        notification = Notificacion(
            user_id=user,
            descripcion=message,
            tipo=tipo,
            fecha=timezone.now()
        )
        notification.save()
        return notification

    def get_notificaciones(self, user):
        """
        Obtiene todas las notificaciones para un usuario específico.
        
        :param user: Usuario del cual obtener las notificaciones.
        :return: QuerySet de notificaciones.
        """
        return Notificacion.objects.filter(user=user).order_by('-fecha')
    
    # Función auxiliar para obtener una instancia de NotificationManager
    def get_notification_manager():
        return NotificationManager()