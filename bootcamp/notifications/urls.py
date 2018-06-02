from django.conf.urls import url

from bootcamp.notifications import views

app_name = 'notifications'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.NotificationUnreadListView.as_view(),
        name='unread'
    ),
    url(
        regex=r'^mark-as-read/(?P<slug>[-\w]+)/$',
        view=views.mark_as_read,
        name='mark_as_read'
    ),
    url(
        regex=r'^mark-all-as-read/$',
        view=views.mark_all_as_read,
        name='mark_all_read'
    ),
    url(
        regex=r'^latest-notifications/$',
        view=views.get_latest_notifications,
        name='latest_notifications'
    ),
]
