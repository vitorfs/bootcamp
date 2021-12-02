from django.conf.urls import url

from bootcamp.notifications import views

app_name = "notifications"
urlpatterns = [
    url(r"^$", views.NotificationUnreadListView.as_view(), name="unread"),
    url(r"^mark-as-read/(?P<slug>[-\w]+)/$", views.mark_as_read, name="mark_as_read"),
    url(r"^mark-as-read-ajax/$", views.mark_as_read_ajax, name="mark_as_read_ajax"),
    url(r"^mark-all-as-read/$", views.mark_all_as_read, name="mark_all_read"),
    url(
        r"^latest-notifications/$",
        views.get_latest_notifications,
        name="latest_notifications",
    ),
    url(
        r"^unread-notifications/$",
        views.get_unread_notifications,
        name="unread_notifications",
    ),
]
