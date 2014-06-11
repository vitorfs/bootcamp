from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.articles.views',
    url(r'^$', 'articles', name='articles'),
    url(r'^write/$', 'write', name='write'),
    url(r'^preview/$', 'preview', name='preview'),
    url(r'^drafts/$', 'drafts', name='drafts'),
    url(r'^comment/$', 'comment', name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', 'tag', name='tag'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', 'article', name='article'),
)