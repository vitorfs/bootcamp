$(function () {
    $('#notifications').popover({
        html: true,
        trigger: 'manual',
        container: "body" ,
        placement: "bottom",
    });

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
            $("#notifications").popover('dispose');
        }
        else {
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {
                    $("#notifications").popover('dispose');
                    $("#notifications").popover({
                        html: true,
                        trigger: 'focus',
                        container: "body" ,
                        placement: "bottom",
                        content: data,
                    });
                    $("#notifications").popover('show');
                },
            });
        }
        return false;
    });
});
