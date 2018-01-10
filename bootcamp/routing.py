from channels import include

channel_routing = [
    # Include subrouting from an app with predefined path matching.
    include("bootcamp.activities.routing.websocket_routing",
            path=r"^/notifications/"),
]
