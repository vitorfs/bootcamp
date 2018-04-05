import json

from channels.generic.websocket import WebsocketConsumer


class NotificationsConsumer(WebsocketConsumer):
    """Consumer to manage WebSocket connections for the Notification app."""
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
