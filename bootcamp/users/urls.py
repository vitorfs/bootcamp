from django.conf.urls import url
from allauth.account.views import PasswordChangeView

from . import views

app_name = "users"
urlpatterns = [
    url(regex=r"^$", view=views.UserListView.as_view(), name="list"),
    url(regex=r"^~redirect/$", view=views.UserRedirectView.as_view(), name="redirect"),
    url(regex=r"^~update/$", view=views.UserUpdateView.as_view(), name="update"),
    url(regex=r"^~password/$", view=PasswordChangeView.as_view(), name="account_change_password"),
    url(r'^picture/$', views.picture, name='picture'),
    url(r'^upload_picture/$', views.upload_picture,
        name='upload_picture'),
    url(r'^save_uploaded_picture/$', views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^u/following/$', views.FollowingPageView.as_view(), name='view_following'),
    url(r'^u/followers/$', views.FollowersPageView.as_view(), name='view_all_followers'),
    url(r'^follow_user/(?P<user_id>\d+)/$',
        views.follow_user,
        name='follow_user'),
    url(r'^send_message_request/(?P<user_id>\d+)/$',
        views.send_message_request,
        name='send_message_request'),
    url(r'^accept_message_request/(?P<user_id>\d+)/$',
        views.accept_message_request,
        name='accept_message_request'),
    url(r'^block_spammer/(?P<user_id>\d+)/$',
        views.block_spammer,
        name='block_spammer'),
    url(r'^friends/all/$', views.all_friends, name='all_friends'),
    url(r'^friends/requests/$', views.all_message_requests, name='all_message_requests'),
    url(
        regex=r"^(?P<username>[\w.@+-]+)/$",
        view=views.UserDetailView.as_view(),
        name="detail",
    ),
]
