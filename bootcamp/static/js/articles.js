$(function () {
    $(".publish").click(function () {
        $("input[name='status']").val("P");
        $("#article-form").submit();
    });

    $(".update").click(function () {
        $("input[name='status']").val("P");
        //$("input[name='edited']").prop("checked");
        $("input[name='edited']").val("True");
        $("#article-form").submit();
    });

    $(".draft").click(function () {
        $("input[name='status']").val("D");
        $("#article-form").submit();
    });
});
