from django.conf.urls import url

from bootcamp.notifications.consumers import NotificationsConsumer

websocket_urlpatterns = [
    url(r'^ws-notifications/$', NotificationsConsumer),
]
