$(function () {
  $(".question .panel-body").click(function () {
    var question_id = $(this).closest(".question").attr("question-id");
    location.href = "/questions/" + question_id;
  });
});