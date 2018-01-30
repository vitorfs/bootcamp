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

    function setUserOnlineOffline(username, status) {
        /* This function enables the client to switch the user connection
        status, allowing to show (when implemented the proper functionality)
        if an user is connected or not.
        */
        var elem = $("online-stat-" + username);
        if (elem) {
            if (status === 'online') {
                elem.attr("class", "btn btn-success btn-circle");
            } else {
                elem.attr("class", "btn btn-danger btn-circle");
            }
        }
    }

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
            console.log("User " + event.username + " just " + event.activity)
        } else if (event.activity_type === "message") {
            console.log(event.sender + " has sent a message to " + event.receiver)
            if (currentUser == event.receiver) {
                $("#unread-count").show();
            }
        } else if (event.activity_type === "set_status") {
            console.log('Status changed')
            //setUserOnlineOffline(event.sender, event.status)
        } else {
            $("#notifications").removeClass("new-notifications");
        }
    });
});
