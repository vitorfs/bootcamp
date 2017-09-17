$(function () {
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
