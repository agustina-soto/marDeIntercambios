# Manejo de mensajes WebSocket en consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def send_notification(self, event):
        notification_data = event['notification']
        self.send(text_data=json.dumps(notification_data))
