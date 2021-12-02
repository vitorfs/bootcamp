from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponse,
    HttpResponseBadRequest,
)

from bootcamp.helpers import ajax_required
from bootcamp.notifications.models import Notification


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to show the unread notifications for
    the actual user"""

    model = Notification
    context_object_name = "notification_list"
    template_name = "notifications/notification_list.html"

    def get_queryset(self, **kwargs):
        return self.request.user.notifications.all()


@login_required
def mark_all_as_read(request):
    """View to call the model method which marks as read all the notifications
    directed to the actual user."""
    request.user.notifications.mark_all_as_read()
    _next = request.GET.get("next")
    messages.add_message(
        request,
        messages.SUCCESS,
        _(f"All notifications to {request.user.username} have been marked as read."),
    )

    if _next:
        return redirect(_next)

    return redirect("notifications:unread")


@login_required
def mark_as_read(request, slug=None):
    """View to call the model method which mark as read the provided
    notification."""
    if slug:
        notification = get_object_or_404(Notification, slug=slug)
        notification.mark_as_read()

    messages.add_message(
        request,
        messages.SUCCESS,
        _(f"The notification {notification.slug} was marked as read."),
    )
    _next = request.GET.get("next")

    if _next:
        return redirect(_next)

    return redirect("notifications:unread")


@login_required
@ajax_required
@require_http_methods(["POST"])
def mark_as_read_ajax(request):
    try:
        slug = request.POST["slug"]
        if slug:
            notification = get_object_or_404(Notification, slug=slug)
            notification.mark_as_read()

        return HttpResponse()

    except Exception:
        return HttpResponseBadRequest()


@login_required
def get_latest_notifications(request):
    notifications = request.user.notifications.get_most_recent()
    request.user.notifications.mark_all_as_read()
    return render(
        request, "notifications/most_recent.html", {"notifications": notifications}
    )


@login_required
def get_unread_notifications(request):
    notifications = request.user.notifications.unread()
    return JsonResponse({"unread_notifications": str(len(notifications))})
