from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from bootcamp.notifications.models import Notification


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to show the unread notifications for
    the actual user"""
    model = Notification
    context_object_name = 'notification_list'
    template_name = 'notifications/notification_list.html'

    def get_queryset(self, **kwargs):
        return self.request.user.notifications.unread()


@login_required
def mark_all_as_read(request):
    """View to call the model method which marks as read all the notifications
    directed to the actual user."""
    request.user.notifications.mark_all_as_read()
    _next = request.GET.get('next')
    messages.add_message(request, messages.SUCCESS,
        f'All notifications to {request.user.username} have been marked as read.')

    if _next:
        return redirect(_next)

    return redirect('notifications:unread')


@login_required
def mark_as_read(request, slug=None):
    """View to call the model method which mark as read the provided
    notification."""
    if slug:
        notification = get_object_or_404(Notification, slug=slug)
        notification.mark_as_read()

    messages.add_message(request, messages.SUCCESS,
        f'The notification {notification.slug} has been marked as read.')
    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    return redirect('notifications:unread')


@login_required
def get_latest_notifications(request):
    data = request.user.notifications.serialize_latest_notifications()
    return HttpResponse(data)
