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

    // onmessage management.
    webSocket.listen(function(event) {
        if (event.activity_type === "message") {
            console.log(event.sender + " just sent a new message");
            $("#new-message-" + event.sender).show();
        }
    });

    // Let's keep using the AJAX view for now, it works great actually.
    $("#send").submit(function () {
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
