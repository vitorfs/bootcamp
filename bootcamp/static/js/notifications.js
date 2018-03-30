$(function () {
    $('#notifications').popover({html: true});

    $("#notifications").click(function () {
        if ($(".popover").is(":visible")) {
            $("#notifications").popover('hide');
        }
        else {
            $("#notifications").popover('show');
            $(".popover-content").html("<a href='{% url 'notifications:notification_list' %}'>{% trans 'All notifications' %}</a>")
            // $("#notifications").popover({'html': "<a href='{% url 'notifications:notification_list' %}'>{% trans 'All notifications' %}</a>",});
            // $(".popover").attr('data-content', "<a href='{% url 'notifications:notification_list' %}'>{% trans 'All notifications' %}</a>")
        }
        return false;
    });
});
