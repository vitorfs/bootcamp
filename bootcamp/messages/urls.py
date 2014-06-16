from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.messages.views',
    url(r'^$', 'inbox', name='messages'),
    url(r'^new/$', 'new', name='new_message'),
    url(r'^send/$', 'send', name='send_message'),
    url(r'^delete/$', 'delete', name='delete_message'),
)