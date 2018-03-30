from django.conf.urls import url

from bootcamp.notifications import views

app_name = 'notifications'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.NotificationUnreadListView.as_view(),
        name='unread'
    ),
]
