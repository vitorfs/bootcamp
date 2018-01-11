$(function () {
    $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
        }
        else {
            $("#notifications").popover('show');
            $.ajax({
                url: '/notifications/last/',
                beforeSend: function () {
                    $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
                    $("#notifications").removeClass("new-notifications");
                },
                success: function (data) {
                    $(".popover-content").html(data);
                }
            });
        }
        return false;
    });

    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/notifications/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to notifications stream at: " + ws_path);
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from notifications stream at: " + ws_path);
    };

    webSocket.listen(function(event) {
        // NOTE: We escape JavaScript to prevent XSS attacks.
        // var data = JSON.parse(event);
        // var username = encodeURI(data['username']);
        if (event.activity_type === "notification") {
            $("#notifications").addClass("new-notifications");
            console.log("User " + event.username + " just " + event.activity)
        }
        else {
            $("#notifications").removeClass("new-notifications");
        }
    });
});
