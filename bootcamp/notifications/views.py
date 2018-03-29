from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView  # , DetailView, RedirectView, UpdateView

from bootcamp.notifications.models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
