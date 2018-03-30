from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView  # , DetailView, RedirectView, UpdateView

from bootcamp.notifications.models import Notification


class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to show the unread notifications for
    the actual user"""
    model = Notification
    context_object_name = 'notification_list'
    template_name = 'notifications/notification_list.html'

    def get_queryset(self, **kwargs):
        return self.request.user.notifications.unread()
