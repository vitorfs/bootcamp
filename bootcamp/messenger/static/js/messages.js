$(function () {
    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to inbox stream at: " + ws_path);
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from inbox stream at: " + ws_path);
    };

    webSocket.listen(function(event) {
        if (event.activity_type === "message") {
            console.log(event.sender + " just sent a new message");
            $("#" + event.sender).show();
            /* var usersList = document.getElementsByClassName('list-group-item');
            for (var i=0; i<usersList.length; i++) {
                var receiver = usersList[i].text.trim();
                console.log(receiver)
            } */
        }
    });
    $("#send").submit(function () {
        /*
        webSocket.send({
            'content': "Message",
            'receiver': messageReceiver,
            'sender': currentUser,
            'activity_type': "message",
            'message_count': 1})
        */
        $.ajax({
            url: '/messages/send/',
            data: $("#send").serialize(),
            cache: false,
            type: 'post',
            success: function (data) {
                $(".send-message").before(data);
                $("input[name='message']").val('');
                $("input[name='message']").focus();
                $('.conversation').scrollTop($('.conversation')[0].scrollHeight);
            }
        });
    return false;
    });
});
