from django.conf.urls import url

from bootcamp.messager import views

app_name = "messager"
urlpatterns = [
    url(r"^$", views.MessagesListView.as_view(), name="messages_list"),
    url(r"^send-message/$", views.send_message, name="send_message"),
    url(r"^receive-message/$", views.receive_message, name="receive_message"),
    url(
        r"^unread-messages/$",
        views.get_unread_messages,
        name="unread_messages",
    ),
    url(
        r"^(?P<username>[\w.@+-]+)/$",
        views.ConversationListView.as_view(),
        name="conversation_detail",
    ),
    url(r"^mark-read-messages/$", views.mark_as_read_messages, name="mark_as_read_messages"),
]
