from channels.routing import route
from bootcamp.activities.consumers import ws_connect, ws_disconnect, ws_receive


websocket_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]
