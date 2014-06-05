from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.feeds.views',
    url(r'^$', 'feeds', name='feeds'),
    url(r'^post/$', 'post', name='post'),
    url(r'^like/$', 'like', name='like'),
    url(r'^comment/$', 'comment', name='comment'),
    url(r'^load/$', 'load', name='load'),
    url(r'^check/$', 'check', name='check'),
    url(r'^load_new/$', 'load_new', name='load_new'),
    url(r'^update/$', 'update', name='update'),
    url(r'^track_comments/$', 'track_comments', name='track_comments'),
    url(r'^remove/$', 'remove', name='remove_feed'),
    url(r'^(\d+)/$', 'feed', name='feed'),
)