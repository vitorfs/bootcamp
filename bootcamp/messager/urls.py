from django.conf.urls import url

from bootcamp.messager import views

app_name = "messager"
urlpatterns = [
    url(r"^$", views.MessagesListView.as_view(), name="messages_list"),
    url(r"^send-message/$", views.send_message, name="send_message"),
    url(r"^receive-message/$", views.receive_message, name="receive_message"),
    url(r"^mark-read-messages/$", views.mark_read_messages, name="mark_read_messages"),
    url(
        r"^get-unread-messages/$",
        views.get_unread_messages,
        name="get_unread_messages",
    ),
    url(
        r"^(?P<username>[\w.@+-]+)/$",
        views.ConversationListView.as_view(),
        name="conversation_detail",
    ),
]
