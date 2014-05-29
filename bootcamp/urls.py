from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bootcamp.feeds.views.feeds', name='feeds'),
    url(r'^post/$', 'bootcamp.feeds.views.post', name='post'),
    url(r'^questions/$', 'bootcamp.questions.views.questions', name='questions'),
    url(r'^questions/ask/$', 'bootcamp.questions.views.ask', name='ask'),
    url(r'^admin/', include(admin.site.urls)),
)
