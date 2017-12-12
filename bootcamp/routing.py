from channels import include

channel_routing = [
    # Include sub-routing from an app with predefined path matching.
    include("bootcamp.messenger.routing.websocket_routing",
            path=r"^/messenger/inbox"),
]
