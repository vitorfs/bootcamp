from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationsConsumer(AsyncWebsocketConsumer):
    """Consumer to manage WebSocket connections for the Notification app,
    called when the websocket is handshaking as part of initial connection.
    """
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()

        else:
            # Accept the connection
            await self.channel_layer.group_add(
                'notifications', self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
           'notifications', self.channel_name)
