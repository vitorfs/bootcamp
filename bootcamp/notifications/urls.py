from django.conf.urls import url

from . import views

app_name = 'notifications'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.NotificationListView.as_view(),
        name='notification_list'
    ),
]
