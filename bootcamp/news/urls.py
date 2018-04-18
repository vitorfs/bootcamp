from django.conf.urls import url

from bootcamp.news import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='list'),
    url(r'^post/$', views.post, name='post_new'),
]
