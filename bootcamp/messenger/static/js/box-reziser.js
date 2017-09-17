function adjustWidth() {
    var parentwidth = $("#chat-container").width();
    $(".chat-box").width(parentwidth);
  }

adjustWidth();

$(window).resize(function() {
    adjustWidth();
});
