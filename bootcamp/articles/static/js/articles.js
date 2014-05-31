$(function () {
  $(".publish").click(function () {
    $("input[name='status']").val("P");
    $("form").submit();
  });

  $(".draft").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });
});