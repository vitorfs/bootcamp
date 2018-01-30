$(function () {
    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

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
        if (event.activity_type === "message") {
            console.log("A new message from " + event.sender);
            if (event.sender === activeUser) {
                addNewMessage(event.message_id);
            } else {
                $("#new-message-" + event.sender).show();
            }
        }
    });

    $("#send").submit(function () {
        /*
        I'll keep the WebSocket data structure idle by now because I haven't
        been able to find a really suitable way to print the new message to
        the client side, and will keep using the AJAX view for now, it works
        great to left it alone for now.

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
