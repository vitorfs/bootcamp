from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'bootcamp.core.views.home', name='home'),
    url(r'^login/$', 'bootcamp.auth.views.login', name='login'),
    url(r'^logout/$', 'bootcamp.auth.views.logout', name='logout'),
    url(r'^signup/$', 'bootcamp.auth.views.signup', name='signup'),
    url(r'^settings/$', 'bootcamp.core.views.settings', name='settings'),
    url(r'^settings/picture/$', 'bootcamp.core.views.picture', name='picture'),
    url(r'^settings/password/$', 'bootcamp.core.views.password', name='password'),
    url(r'^network/$', 'bootcamp.core.views.network', name='network'),
    url(r'^feeds/', include('bootcamp.feeds.urls')),
    url(r'^questions/', include('bootcamp.questions.urls')),
    url(r'^articles/', include('bootcamp.articles.urls')),
    url(r'^(?P<username>[^/]+)/$', 'bootcamp.core.views.profile', name='profile'),
)
