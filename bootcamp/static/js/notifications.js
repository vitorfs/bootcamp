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
        }
        else {
            $("#notifications").popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                beforeSend: function () {
                    //$("#notifications").popover("dispose");
                    $("#notifications").popover({
                        html: true,
                        trigger: 'manual',
                        container: "body" ,
                        placement: "bottom",
                        content: "Text",// "<div style='text-align:center'><img src='/static/img/loading.gif'></div>",
                    }).popover("show");
                    //$("#notifications").popover("show");
                    console.log('This is being done!')
                    // $(this).attr('data-content', "<div style='text-align:center'><img src='/static/img/loading.gif'></div>");

                },
                success: function (data) {
                    $(this).attr('data-content', data);
                    console.log('Loaded')
                }
            });
        }
        return false;
    });
});
/*
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
        }
        else {
            $("#notifications").popover('show');
            $.ajax({
                url: '/notifications/latest-notifications/',
                beforeSend: function () {
                    $(".popover-content").html("<div style='text-align:center'><img src='/static/img/loading.gif'></div>");
                },
                success: function (data) {
                    $(".popover-content").html(data);
                }
            });
        }
        return false;
    });
});
 */
