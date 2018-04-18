from django.conf.urls import url

from bootcamp.news import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='list'),
    url(r'^delete/(?P<pk>[-\w]+)/$',
        views.NewsDeleteView.as_view(), name='delete_news'),
    url(r'^post/$', views.post, name='post_new'),
    url(r'^like/$', views.like, name='like_post'),
]
