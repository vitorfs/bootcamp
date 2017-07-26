from django.conf.urls import url

from bootcamp.articles import views

urlpatterns = [
    url(r'^$', views.articles, name='articles'),
    url(r'^write/$', views.CreateArticle.as_view(), name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<pk>\d+)/$',
        views.EditArticle.as_view(), name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]
