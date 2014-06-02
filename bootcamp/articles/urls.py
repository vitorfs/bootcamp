from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.articles.views',
    url(r'^$', 'articles', name='articles'),
    url(r'^(?P<slug>[-\w]+)/$', 'article', name='article'),
    url(r'^write/$', 'write', name='write'),
    url(r'^drafts/$', 'drafts', name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', 'tag', name='tag'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_article'),
)