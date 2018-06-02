$(function () {
    function hide_stream_update() {
        $(".stream-update").hide();
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
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Focus on the modal input by default.
    $('#newsFormModal').on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });

    $('#newsThreadModal').on('shown.bs.modal', function () {
        $('#replyInput').trigger('focus')
    });

    // Counts textarea characters to provide data to user.
    $("#newsInput").keyup(function () {
        var charCount = $(this).val().length;
        $("#newsCounter").text(280 - charCount);
    });

    $("#replyInput").keyup(function () {
        var charCount = $(this).val().length;
        $("#replyCounter").text(280 - charCount);
    });

    $("input, textarea").attr("autocomplete", "off");

    $("#postNews").click(function () {
        // Ajax call after pushing button, to register a News object.
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
        // Ajax call to register a reply to any given News object.
        $.ajax({
            url: '/news/post-comment/',
            data: $("#replyNewsForm").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                $("#replyInput").val("");
                $("#newsThreadModal").modal("hide");
            },
            error: function(data){
                alert(data.responseText);
            },
        });
    });

    $("ul.stream").on("click", ".like", function () {
        // Ajax call on action on like button.
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
        // Ajax call to request a given News object detail and thread, and to
        // show it in a modal.
        var post = $(this).closest(".card");
        var news = $(post).closest("li").attr("news-id");
        $("#newsThreadModal").modal("show");
        $.ajax({
            url: '/news/get-thread/',
            data: {'news': news},
            cache: false,
            beforeSend: function () {
                $("#threadContent").html("<li class='loadcomment'><img src='/static/img/loading.gif'></li>");
            },
            success: function (data) {
                $("input[name=parent]").val(data.uuid)
                $("#newsContent").html(data.news);
                $("#threadContent").html(data.thread);
            }
        });
        return false;
    });
});


/* Example query for the GraphQL endpoint.

    query{
        news(uuidId: "--insert here the required uuid_id value for the lookup"){
          uuidId
          content
          timestamp
          countThread
          countLikers
          user {
            name
            picture
          }
          liked {
            name
          }
          thread{
            content
          }
        }
        paginatedNews(page: 1){
          page
          pages
          hasNext
          hasPrev
          objects {
            uuidId
            content
            timestamp
            countThread
            countLikers
            user {
              name
              picture
            }
            liked {
              name
            }
            thread{
              content
            }
          }
        }
      }
 */
