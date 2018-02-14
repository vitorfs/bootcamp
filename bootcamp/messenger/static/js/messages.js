$(function () {
    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    function setUserOnlineOffline(username, status) {
        /* This function enables the client to switch the user connection
        status, allowing to show if an user is connected or not.
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

    function scrollConversationScreen() {
        /* Set focus on the input box from the form, and rolls to show the
        the most recent message.
        */
        $("input[name='message']").focus();
        $('.conversation').scrollTop($('.conversation')[0].scrollHeight);
    }

    function addNewMessage(message_id) {
        /* This function calls the respective AJAX view, so it will be able to
        load the received message in a proper way.
         */
        $.ajax({
            url: '/messages/receive/',
            data: {'message_id': message_id},
            cache: false,
            success: function (data) {
                $(".send-message").before(data);
                scrollConversationScreen();
            }
        });
    }

    window.onbeforeunload = function () {
        // Small function to run instruction just before closing the session.
        payload = {
            'sender': currentUser,
            'activity_type': "set_status",
            'status': 'offline'
        }
        webSocket.send(payload);
    }

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to inbox stream");
        payload = {
            'sender': currentUser,
            'activity_type': "set_status",
            'status': 'online'
        }
        webSocket.send(payload);
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from inbox stream");
    };

    // onmessage management.
    webSocket.listen(function(event) {
        switch (event.activity_type) {
            case "message":
                if (event.sender === activeUser) {
                    addNewMessage(event.message_id);
                    // I hope there is a more elegant way to work this out.
                    setTimeout(function(){$("#unread-count").hide()}, 1);
                } else {
                    $("#new-message-" + event.sender).show();
                }
                break;
            case "set_status":
                setUserOnlineOffline(event.sender, event.status)
                break;
            default:
                console.log('error: ', event)
                break;
        }
    });

    $("#send").submit(function () {
        /*
        WebSocket data structure idle by now waiting for way to print the new
        message to the client side.

        payload = {
                'sender': currentUser,
                'receiver': activeUser,
                'message': $("input[name='message']").val()
            }
        webSocket.send(payload); */
        $.ajax({
            url: '/messages/send/',
            data: $("#send").serialize(),
            cache: false,
            type: 'post',
            success: function (data) {
                $(".send-message").before(data);
                $("input[name='message']").val('');
                scrollConversationScreen();
            }
        });
        return false;
    });
});
