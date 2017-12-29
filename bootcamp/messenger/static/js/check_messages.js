$(function () {
    function check_messages() {
        $.ajax({
            url: '/messages/check/',
            cache: false,
            success: function (data) {
                $("#unread-count").text(data);
            },
            complete: function () {
                window.setTimeout(check_messages, 60000);
            }
        });
    }
    check_messages();
});

$(function () {
    var message_text = $("input[name='message']").val();
    // Correctly decide between ws:// and wss://
    // var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    // var ws_path = ws_scheme + '://' + window.location.host + "/messenger/inbox/";
    var ws_path = "/messenger/inbox/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);
    console.log("Connecting to " + ws_path);

    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    webSocket.socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };
    webSocket.socket.onmessage = function(event) {
        // Handle errors
        if (event.error) {
            alert(event.error);
            return;
        }
        // Decode the JSON
        console.dir(event);
        // var data = JSON.parse(event);
        console.log("Got websocket data:", event);
        // Handle joining
        if (event.message) {
            console.log(event.text);

        } else {
            console.log("Cannot handle message!");
        }
    };
});
