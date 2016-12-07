from django.conf.urls import url

from bootcamp.messenger import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^new/$', views.new, name='new_message'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^users/$', views.users, name='users_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
]
