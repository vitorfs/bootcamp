$(function () {
  $(".btn-compose").click(function () {
    $(".compose textarea").val("");
    $(".compose").slideDown(400, function () {
      $(".compose textarea").focus();
    });
  });

  $(".btn-cancel-compose").click(function () {
    $(".compose").slideUp();
  });

  $(".btn-post").click(function () {
    $.ajax({
      url: '/feeds/post/',
      data: $("#compose-form").serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("ul.stream").prepend(data);
        $(".compose").slideUp();
      }
    });
  });

  $("ul.stream").on("click", ".like", function () {
    var li = $(this).closest("li");
    var feed = $(li).attr("feed-id");
    var csrf = $(li).attr("csrf");
    $.ajax({
      url: '/feeds/like/',
      data: {
        'feed': feed,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
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
        $(".like .like-count", li).text(data);
      }
    });
    return false;
  });

  $("ul.stream").on("click", ".comment", function () { 
    var post = $(this).closest(".post");
    $(".comments", post).slideDown();
    return false;
  });
});