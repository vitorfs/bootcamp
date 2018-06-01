$(function () {
    function hide_stream_update() {
        $(".stream-update").hide();
        $(document).attr("title", page_title);
    };

    function getCookie(name) {
        // Function to get any cookie available in the session.
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    var page_title = $(document).attr("title");
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('#newsFormModal').on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });

    $('#newsThreadModal').on('shown.bs.modal', function () {
        $('#replyInput').trigger('focus')
    });

    $("#newsInput").keyup(function () {
        var charCount = $(this).val().length;
        $(".text-counter-block").text(280 - charCount);
    });

    $("input, textarea").attr("autocomplete", "off");

    $("#postNews").click(function () {
        $.ajax({
            url: '/news/post-news/',
            data: $("#postNewsForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("ul.stream").prepend(data);
                $("#newsInput").val("");
                $("#newsFormModal").modal("hide");
                hide_stream_update();
            },
            error : function(data){
                alert(data.responseText);
            },
        });
    });

    $("#replyNews").click(function () {
        console.log("Replied");
        /* $.ajax({
            url: '/news/post-comment/',
            data: $("#replyNewsForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                console.log("Success")
                console.log(data)
            },
            error : function(data){
                alert(data.responseText);
            },
        }); */
    });

    $("ul.stream").on("click", ".like", function () {
        var li = $(this).closest("li");
        var news = $(li).attr("news-id");
        payload = {
            'news': news,
            'csrf_token': csrftoken
        }
        $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like .like-count", li).text(data.likes);
                if ($(".like .heart", li).hasClass("fa fa-heart")) {
                    $(".like .heart", li).removeClass("fa fa-heart");
                    $(".like .heart", li).addClass("fa fa-heart-o");
                } else {
                    $(".like .heart", li).removeClass("fa fa-heart-o");
                    $(".like .heart", li).addClass("fa fa-heart");
                }
            }
        });
        return false;
    });

    $("ul.stream").on("click", ".comment", function () {
        var post = $(this).closest(".card");
        var news = $(post).closest("li").attr("news-id");
        $("#newsThreadModal").modal("show");
        $.ajax({
            url: '/news/get-comments/',
            data: {'news': news},
            cache: false,
            beforeSend: function () {
                $("#threadContent").html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
            },
            success: function (data) {
                $("#threadContent").html(data);
            }
        });
        return false;
    });

    $("ul.stream").on("keydown", ".comments input[name='post']", function (evt) {
        var keyCode = evt.which?evt.which:evt.keyCode;
        if (keyCode == 13) {
            var form = $(this).closest("form");
            var container = $(this).closest(".comments");
            var input = $(this);
            var post = $(this).closest(".post");
            $.ajax({
                url: '/news/post-comment/',
                data: $(form).serialize(),
                type: 'POST',
                cache: false,
                beforeSend: function () {
                    $(input).val("");
                },
                success: function (data) {
                    $(".comments", post).slideUp();
                    var post_container = $(container).closest(".post");
                    $(".comment-count", post_container).text(data.comments);
                }
            });
            return false;
        }
    });
});
