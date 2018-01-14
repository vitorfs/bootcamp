from channels import route

from bootcamp.messenger.consumers import ws_connect, ws_receive, ws_disconnect


websocket_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_receive),
    route("websocket.disconnect", ws_disconnect),
]
