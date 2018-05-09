from django.conf.urls import url

from bootcamp.messager import views

app_name = 'messager'
urlpatterns = [
    url(r'^$', views.MessagesListView.as_view(), name='messages_list'),
]
