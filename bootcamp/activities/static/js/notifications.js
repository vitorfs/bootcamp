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
        console.log("Connected to notifications stream");
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from notifications stream");
    };

    webSocket.listen(function(event) {
        if (event.activity_type === "notification") {
            $("#notifications").addClass("new-notifications");
        } else if (event.activity_type === "message") {
            if (currentUser == event.receiver) {
                $("#unread-count").show();
            }
        }
    });
});
