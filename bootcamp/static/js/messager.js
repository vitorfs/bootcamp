$(function () {

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
            };
        };
    };

    function addNewMessage(message_id) {
        /* This function calls the respective AJAX view, so it will be able to
        load the received message in a proper way.
         */
        $.ajax({
            url: '/messages/receive-message/',
            data: {'message_id': message_id},
            cache: false,
            success: function (data) {
                $(".send-message").before(data);
                scrollConversationScreen();
            }
        });
    };

    function scrollConversationScreen() {
        /* Set focus on the input box from the form, and rolls to show the
        the most recent message.
        */
        $("input[name='message']").focus();
        $('.conversation').scrollTop($('.conversation')[0].scrollHeight);
    }

    $("#send").submit(function () {
        $.ajax({
            url: '/messages/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: 'POST',
            success: function (data) {
                $(".send-message").before(data);
                $("input[name='message']").val('');
                scrollConversationScreen();
            }
        });
        return false;
    });

    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    window.onbeforeunload = function () {
        // Small function to run instruction just before closing the session.
        payload = {
            "type": "recieve",
            "sender": currentUser,
            "set_status": "offline"
        };
        webSocket.send(payload);
    }

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to inbox stream");
        // Commenting this block until I find a better way to manage how to
        // report the user status.

        /* payload = {
            "type": "recieve",
            "sender": currentUser,
            "set_status": "online"
        };
        webSocket.send(payload); */
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from inbox stream");
    };

    // onmessage management.
    webSocket.listen(function(event) {
        switch (event.key) {
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
                setUserOnlineOffline(event.sender, event.status);
                break;

            default:
                console.log('error: ', event);
                console.log(typeof(event))
                break;
        }
    });
});
