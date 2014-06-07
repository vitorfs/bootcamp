$(function () {
  $(".feed-results li").click(function () {
    var feed = $(this).attr("feed-id");
    location.href = "/feeds/" + feed + "/";
  });

  $(".articles-results li").click(function () {
    var article = $(this).attr("article-slug");
    location.href = "/articles/" + article + "/";
  });

  $(".questions-results li").click(function () {
    var question = $(this).attr("question-id");
    location.href = "/questions/" + question + "/";
  });

});