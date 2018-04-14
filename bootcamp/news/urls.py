from django.conf.urls import url

from bootcamp.news import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='list'),
]
