from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = patterns('bootcamp.articles.views',
    url(r'^$', login_required(ArticlesList.as_view(), login_url='/login'), name='articles'),
    url(r'^write/$', 'write', name='write'),
    url(r'^drafts/$', 'drafts', name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', 'tag', name='tag'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', 'article', name='article'),
)
