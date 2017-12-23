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
    // Correctly decide between ws:// and wss://
    var ws_path = "/messenger/inbox/";
    console.log("Connecting to " + ws_path);
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);
    // Handle incoming messages
    webSocket.listen(function(data) {
        // Decode the JSON
        console.log("Got websocket message", data);
        // Handle errors
        if (data.error) {
            alert(data.error);
            return;
        }
        // Handle joining
        if (data.join) {
            console.log("Joining room " + data.join);
            var roomdiv = $(
                    "<div class='room' id='room-" + data.join + "'>" +
                    "<h2>" + data.title + "</h2>" +
                    "<div class='messages'></div>" +
                    "<form><input><button>Send</button></form>" +
                    "</div>"
            );
            // Hook up send button to send a message
            roomdiv.find("form").on("submit", function () {
                webSocket.send({
                    "command": "send",
                    "room": data.join,
                    "message": roomdiv.find("input").val()
                });
                roomdiv.find("input").val("");
                return false;
            });
            $("#chats").append(roomdiv);
            // Handle leaving
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
            // Handle getting a message
        } else if (data.message) {
            var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            ok_msg_two = "<div class='message'>" +
                         "<span class='username'>" + data.username + "</span>" +
                         "<span class='body'>" + data.message + "</span>" +
                         "</div>";
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
        } else {
            console.log("Cannot handle message!");
        }
    });
    // Room join/leave
    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            // Leave room
            $(this).removeClass("joined");
            webSocket.send({
                "command": "leave",
                "room": roomId
            });
        } else {
            // Join room
            $(this).addClass("joined");
            webSocket.send({
                "command": "join",
                "room": roomId
            });
        }
    });
    // Helpful debugging
    webSocket.socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    webSocket.socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };
});
