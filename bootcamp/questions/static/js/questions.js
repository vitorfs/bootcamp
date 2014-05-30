$(function () {
  $(".question .panel-body").click(function () {
    var question_id = $(this).closest(".question").attr("question-id");
    location.href = "/questions/" + question_id;
  });

  $(".accept").click(function () {
    var span = $(this);
    var question = $(".question").attr("question-id");
    var answer = $(this).closest(".answer").attr("answer-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".answer")).val();
    $.ajax({
      url: '/questions/answer/accept/',
      data: {
        'question': question,
        'answer': answer,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(".accept").removeClass("accepted");
        $(span).addClass("accepted");
      }
    });
  });

  $(".vote").click(function () {
    var span = $(this);
    var answer = $(this).closest(".answer").attr("answer-id");
    var csrf = $("input[name='csrfmiddlewaretoken']", $(this).closest(".answer")).val();
    var vote = "";
    if ($(this).hasClass("up-vote")) {
      vote = "U";
    }
    else if ($(this).hasClass("down-vote")) {
      vote = "D";
    }
    $.ajax({
      url: '/questions/answer/vote/',
      data: {
        'answer': answer,
        'vote': vote,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        var options = $(span).closest('.options');
        $('.vote', options).removeClass('voted');
        if (vote == 'U' || vote == 'D') {
          $(span).addClass('voted');
        }
        $('.votes', options).text(data);
      }
    });
  });

  $("[data-toggle='tooltip']").tooltip();
});