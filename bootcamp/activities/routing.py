from channels.routing import route
from bootcamp.activities.consumers import ws_connect, ws_disconnect


websocket_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]
