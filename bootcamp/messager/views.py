from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from bootcamp.messager.models import Message


class MessagesListView(LoginRequiredMixin, ListView):
    """CBV to render the index view
    """
    model = Message
    paginate_by = 100
    template_name = "messager/message_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(
            MessagesListView, self).get_context_data(*args, **kwargs)
        context['users_list'] = get_user_model().objects.filter(
            is_active=True).exclude(
                username=self.request.user).order_by('username')
        context['active'] = Message.objects.get_most_recent_conversation(
            self.request.user
        )
        return context

    def get_queryset(self):
        active_user = Message.objects.get_most_recent_conversation(
            self.request.user)
        return Message.objects.get_conversation(active_user, self.request.user)
