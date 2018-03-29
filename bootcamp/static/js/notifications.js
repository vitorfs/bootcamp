$(function () {
    $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
        }
        else {
            var longtest = 'This is not precisely the longest text I can come over, but it will do.'
            $("#notifications").popover('show');
        }
        return false;
    });
});
