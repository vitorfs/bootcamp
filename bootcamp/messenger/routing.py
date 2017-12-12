from channels import route

from bootcamp.messenger.consumers import ws_connect, ws_receive, ws_disconnect


websocket_routing = [
    # Called when WebSockets connect
    route("websocket.connect", ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect),
]
