from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = patterns('bootcamp.articles.views',
    url(r'^$', login_required(ArticlesList.as_view(), login_url='/login'), name='articles'),
    url(r'^new/$', login_required(ArticleCreateView.as_view(), login_url='/login'), name='write'),
    url(r'^drafts/$', login_required(ArticlesDraftListView.as_view(), login_url='/login'), name='drafts'),
    url(r'^tag/(?P<tag_name>.+)/$', login_required(ArticleTagView.as_view(), login_url='/login'), name='tag'),
    url(r'^preview/$', 'preview', name='preview'),
    url(r'^comment/$', 'comment', name='comment'),
    url(r'^edit/(?P<id>\d+)/$', 'edit', name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', login_required(ArticleView.as_view(), login_url='/login'), name='article'),
)
