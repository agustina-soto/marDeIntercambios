import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from Aplicaciones.Modelos.models import Usuario, Room, Message

# Definimos la clase ChatConsumer que hereda de AsyncWebsocketConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None  # Nombre de la sala de chat
        self.room_group_name = None  # Nombre del grupo de la sala de chat

    # Método asíncrono que se llama cuando el cliente se conecta
    async def connect(self):
        self.room_name = self.scope['path'].strip('/ws/')  # Obtenemos el nombre de la sala desde la URL
        self.room_group_name = "chat_%s" % self.room_name  # Definimos el nombre del grupo de la sala

        # Añadimos el canal del cliente al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptamos la conexión WebSocket
        await self.accept()

    # Método asíncrono que se llama cuando el cliente se desconecta
    async def disconnect(self, close_code):
        # Quitamos el canal del cliente del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Método que devuelve el nombre del canal del cliente
    def get_channel_name(self):
        return self.channel_name

    # Método asíncrono que se llama cuando el cliente envía un mensaje
    async def receive(self, text_data):
        data = json.loads(text_data)  # Convertimos el texto JSON en un diccionario
        message = data["message"]  # Obtenemos el mensaje
        username = data["username"]  # Obtenemos el nombre de usuario
        room = data["room"]  # Obtenemos el nombre de la sala

        # Guardamos el mensaje en la base de datos
        await self.save_messages(username, room, message)

        # Enviamos el mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "send_message",  # Tipo de evento
                "message": message,  # Mensaje
                "username": username,  # Nombre de usuario
                "room": room  # Sala
            })

    # Método asíncrono para enviar un mensaje al cliente
    async def send_message(self, event):
        username = event["username"]  # Obtenemos el nombre de usuario
        room = event["room"]  # Obtenemos la sala
        message = event["message"]  # Obtenemos el mensaje

        # Enviamos el mensaje al cliente
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "room": room
        }))

    # Método para guardar los mensajes en la base de datos
    @sync_to_async
    def save_messages(self, username, room, message):
        _user = Usuario.objects.get(username=username)  # Obtenemos el usuario desde la base de datos
        _room = Room.objects.get(slug=room)  # Obtenemos la sala desde la base de datos

        # Creamos un nuevo mensaje y lo guardamos en la base de datos
        Message.objects.create(user=_user, room=_room, content=message)
