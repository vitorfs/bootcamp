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
      url: '/post/',
      data: $("#compose-form").serialize(),
      type: 'post',
      cache: false,
      success: function (data) {
        $("ul.stream").prepend(data);
        $(".compose").slideUp();
      }
    });
  });
});