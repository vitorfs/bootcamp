$(function () {
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/inbox/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to messaging stream at: " + ws_path);
    };

    webSocket.socket.onclose = function () {
        console.log("Disconnected from messaging stream at: " + ws_path);
    };

    webSocket.listen(function(event) {
        console.log(event.sender + " has sent a message to " + event.receiver)
        $("#unread-count").text(event.message_count);
            /* Commenting while I choose an approach to solve it.
            $.ajax({
                url: '/messages/check/',
                cache: false,
                success: function (data) {
                    $("#unread-count").text(data);
                },
            });
            */
    });
});
