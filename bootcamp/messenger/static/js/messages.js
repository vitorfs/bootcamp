$(function () {
    // WebSocket connection management block.
    // Correctly decide between ws:// and wss://
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/" + currentUser + "/";
    var webSocket = new channels.WebSocketBridge();
    webSocket.connect(ws_path);

    function addNewMessage() {
        var messageElem =
            $('<li>' +
                '<img src="{{ message.from_user.profile.get_picture }}" class="picture">' +
                '<div>' +
                '<h5>' +
                    '<small class="pull-right">' +
                    '{{ message.date|date:"N d G:i" }}' +
                    '</small>' +
                    '<b>' +
                    '<a href="{% url "profile" message.from_user.username %}">' +
                        '{{ message.from_user.profile.get_screen_name }}' +
                    '</a>' +
                    '</b>' +
                '</h5>' +
                '{{ message.message }}' +
                '</div>' +
            '</li>')
        $(".conversation").append(messageElem);
    }

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
            if (event.sender === activeUser) {
                // addNewMessage();
                $('.conversation').scrollTop($('.conversation')[0].scrollHeight);
            } else {
                $("#new-message-" + event.sender).show();
            }
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
