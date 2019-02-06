from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from bootcamp.messager.models import Message
from bootcamp.helpers import ajax_required
from bootcamp.notifications.models import Notification, notification_handler

class MessagesListView(LoginRequiredMixin, ListView):
    """CBV to render the inbox, showing by default the most recent
    conversation as the active one.
    """
    model = Message
    paginate_by = 501
    template_name = "messager/message_list.html"


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['users_list'] = get_user_model().objects.filter(
        #     is_active=True).exclude(
        #         username=self.request.user).order_by('username')
        msg_user_list = Message.objects.raw("SELECT * FROM messager_message WHERE recipient_id = '" + str(self.request.user.id) + "' OR sender_id = '" + str(self.request.user.id) + "'")
        users_list = "-1"
        for msg_user_item in msg_user_list:
            users_list = users_list + "," + str(msg_user_item.recipient_id) + "," + str(msg_user_item.sender_id)
        context['users_list'] = get_user_model().objects.raw("SELECT * FROM users_user WHERE is_active=TRUE AND id in (" + users_list + ") and username != '" + self.request.user.username + "'")
        last_conversation = Message.objects.get_most_recent_conversation(
            self.request.user
        )
        context['active'] = last_conversation.username
        return context

    def get_queryset(self):
        active_user = Message.objects.get_most_recent_conversation(
            self.request.user)
        return Message.objects.get_conversation(active_user, self.request.user)


class ConversationListView(MessagesListView):
    """CBV to render the inbox, showing an specific conversation with a given
    user, who requires to be active too."""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]
        return context

    def get_queryset(self):
        active_user = get_user_model().objects.get(
            username=self.kwargs["username"])

        return Message.objects.get_conversation(active_user, self.request.user)


@login_required
@ajax_required
@require_http_methods(["POST"])
def send_message(request):
    """AJAX Functional view to recieve just the minimum information, process
    and create the new message and return the new data to be attached to the
    conversation stream."""
    sender = request.user
    recipient_username = request.POST.get('to')
    recipient = get_user_model().objects.get(username=recipient_username)
    message = request.POST.get('message')
    if len(message.strip()) == 0:
        return HttpResponse()

    if sender != recipient:
        msg = Message.send_message(sender, recipient, message)
        notification_handler(sender, recipient, Notification.REPLY)

        return render(request, 'messager/single_message.html',
                      {'message': msg})

    return HttpResponse()


@login_required
@ajax_required
@require_http_methods(["GET"])
def receive_message(request):
    """Simple AJAX functional view to return a rendered single message on the
    receiver side providing realtime connections."""
    message_id = request.GET.get('message_id')
    message = Message.objects.get(pk=message_id)
    return render(request,
                  'messager/single_message.html', {'message': message})
