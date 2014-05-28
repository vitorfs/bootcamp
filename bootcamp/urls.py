from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bootcamp.core.views.home', name='home'),
    url(r'^post/$', 'bootcamp.feeds.views.post', name='post'),
    url(r'^admin/', include(admin.site.urls)),
)
