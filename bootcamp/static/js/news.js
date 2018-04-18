$(function () {
    var page_title = $(document).attr("title");
    $(".btn-cancel-compose").click(function () {
        $(".compose").slideUp();
    });
    $("input,textarea").attr("autocomplete", "off");
    $("#compose-form textarea[name='post']").keyup(function () {
        var charCount = $(this).val().length;
        $(".help-block").text(280 - charCount);
    });

    function hide_stream_update() {
        $(".stream-update").hide();
        $(".stream-update .new-posts").text("");
        $(document).attr("title", page_title);
    };

    function update_news () {
        var first_news = $(".stream li:first-child").attr("news-id");
        var last_news = $(".stream li:last-child").attr("news-id");
        var news_source = $("#news_source").val();

        if (first_news != undefined && last_news != undefined) {
            $.ajax({
                url: '/news/update/',
                data: {
                    'first_news': first_news,
                    'last_news': last_news,
                    'news_source': news_source
                },
                cache: false,
                success: function (data) {
                    $.each(data, function(id, news) {
                            var li = $("li[news-id='" + id + "']");
                            $(".like-count", li).text(news.likes);
                            $(".comment-count", li).text(news.comments);
                    });
                },
            });
        }
    };

    function track_comments () {
        $(".tracking").each(function () {
            var container = $(this);
            var news = $(this).closest("li").attr("news-id");
            $.ajax({
                url: '/news/track_comments/',
                data: {'news': news},
                cache: false,
                success: function (data) {
                    if (data != 0) {
                        $("ol", container).html(data);
                        var post_container = $(container).closest(".post");
                        $(".comment-count", post_container).text($("ol li", container).length);
                    }
                }
            });
        });
    };

    function check_new_news () {
        var last_news = $(".stream li:first-child").attr("news-id");
        var news_source = $("#news_source").val();
        if (last_news != undefined) {
            $.ajax({
                url: '/news/check/',
                data: {
                    'last_news': last_news,
                    'news_source': news_source
                },
                cache: false,
                success: function (data) {
                    if (parseInt(data) > 0) {
                        $(".stream-update .new-posts").text(data);
                        $(".stream-update").show();
                        $(document).attr("title", "(" + data + ") " + page_title);
                    }
                },
            });
        }
    };

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
            url: '/news/post/',
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
        payload = {'news': news }
        $.ajax({
            url: '/news/like/',
            data: payload,
            cache: false,
            success: function (data) {
                if ($(".like", li).hasClass("unlike")) {
                    $(".like", li).removeClass("unlike");
                    $(".like .text", li).text("Like");
                }
                else {
                    $(".like", li).addClass("unlike");
                    $(".like .text", li).text("Unlike");
                }
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
                data: { 'news': news },
                cache: false,
                beforeSend: function () {
                    console.log('Loading...')
                    $("ol", post).html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
                },
                success: function (data) {
                    console.log(data)
                    $("ol", post).html(data);
                    $(".comment-count", post).text(data.comments);
                }
            });
        }
        return false;
    });
});
