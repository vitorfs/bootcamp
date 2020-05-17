from django.conf.urls import url

from . import views

app_name = "groups"
urlpatterns = [
    url(r'^$', views.GroupsPageView.as_view(), name='view_all_groups'),
    url(r'^(?P<group>[-\w]+)/$',
        views.GroupPageView.as_view(),
        name='group'),
    # url(r'^ban_user/(?P<group>[-\w]+)/(?P<user_id>\d+)/$',
    #         views.ban_user,
    #         name='ban_user'),
    url(r'^(?P<group>[-\w]+)/edit_group_cover/$',
        views.edit_group_cover,
        name='edit_group_cover'),
    url(r'^(?P<group>[-\w]+)/subscription/$',
        views.subscribe,
        name='subscribe'),
    # url(r'^(?P<subject>[-\w]+)/like/$',
    #     views.like_subject,
    #     name='like'),
    url(r'^banned_users/(?P<group>[-\w]+)/$',
        views.banned_users,
        name='banned_users'),
]
