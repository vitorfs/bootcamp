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
      success: function(data) {
        $(".accept").removeClass("accepted");
        $(span).addClass("accepted");
      }
    });
  });

  $("[data-toggle='tooltip']").tooltip();
});