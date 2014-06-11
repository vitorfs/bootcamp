from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.messages.views',
    url(r'^$', 'inbox', name='messages'),
    url(r'^inbox/$', 'inbox', name='inbox'),
    url(r'^sent/$', 'sent', name='sent'),
    url(r'^compose/$', 'compose', name='compose'),
    url(r'^delete/$', 'delete', name='delete_message'),
    url(r'^(\d+)/reply/$', 'reply', name='reply'),
    url(r'^(\d+)/$', 'message', name='message'),
)