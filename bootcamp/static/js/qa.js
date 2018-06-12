$(function () {
    $("#publish").click(function () {
        $("input[name='status']").val("O");
        $("#question-form").submit();
    });

    $("#draft").click(function () {
        $("input[name='status']").val("D");
        $("#question-form").submit();
    });
});
