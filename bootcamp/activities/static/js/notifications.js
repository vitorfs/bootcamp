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
        /*
            Left this block of code here to keep it in mind to fix the issue
            with the notification snippet not working in a way of liking.
            I guess I would need to create an issue in the project.

            $.ajax({
                url: '/notifications/check/',
                cache: false,
                success: function (data) {
                    if (data != "0") {
                        $("#notifications").addClass("new-notifications");
                    }
                    else {
                        $("#notifications").removeClass("new-notifications");
                    }
                },
            });
        */
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from notifications stream at: " + ws_path);
    };

    webSocket.listen(function(event) {
        if (event.activity_type === "notification") {
            $("#notifications").addClass("new-notifications");
            console.log("User " + event.username + " just " + event.activity)
        }
        else {
            $("#notifications").removeClass("new-notifications");
        }
    });
});
