$(function () {
    function hide_stream_update() {
        $(".stream-update").hide();
        $(".stream-update .new-posts").text("");
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

    $(".btn-cancel-compose").click(function () {
        $(".compose").slideUp();
    });

    $("input,textarea").attr("autocomplete", "off");

    $("#compose-form textarea[name='post']").keyup(function () {
        var charCount = $(this).val().length;
        $(".help-block").text(280 - charCount);
    });

    $("body").keydown(function (evt) {
        var keyCode = evt.which?evt.which:evt.keyCode;
        if (evt.ctrlKey && keyCode == 80) {
            $(".btn-compose").click();
            return false;
        }
    });

    $("#compose-form textarea[name='post']").keydown(function (evt) {
        var keyCode = evt.which?evt.which:evt.keyCode;
        if (evt.ctrlKey && (keyCode == 10 || keyCode == 13)) {
            $(".btn-post").click();
        }
    });

    $(".btn-compose").click(function () {
        if ($(".compose").hasClass("composing")) {
            $(".compose").removeClass("composing");
            $(".compose").slideUp();
        }
        else {
            $(".compose").addClass("composing");
            $(".compose textarea").val("");
            $(".compose").slideDown(400, function () {
                $(".compose textarea").focus();
            });
        }
    });

    $(".btn-post").click(function () {
        $.ajax({
            url: '/news/post-news/',
            data: $("#compose-form").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("ul.stream").prepend(data);
                $(".compose").slideUp();
                $(".compose").removeClass("composing");
                hide_stream_update();
            },
            error : function(data){
                alert(data.responseText)
            },
        });
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
            }
        });
        return false;
    });

    $("ul.stream").on("click", ".comment", function () {
        var post = $(this).closest(".post");
        if ($(".comments", post).hasClass("tracking")) {
            $(".comments", post).slideUp();
            $(".comments", post).removeClass("tracking");
        }
        else {
            $(".comments", post).show();
            $(".comments", post).addClass("tracking");
            $(".comments input[name='post']", post).focus();
            var news = $(post).closest("li").attr("news-id");
            $.ajax({
                url: '/news/get-comments/',
                data: {'news': news},
                cache: false,
                beforeSend: function () {
                    $("ol", post).html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
                },
                success: function (data) {
                    $("ol", post).html(data);
                    $(".comment-count", post).text(data.comments);
                }
            });
        }
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
                }
            });
            return false;
        }
    });
});
