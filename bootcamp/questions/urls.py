from django.conf.urls import url

from bootcamp.questions import views

urlpatterns = [
    url(r'^$', views.questions, name='questions'),
    url(r'^answered/$', views.answered, name='answered'),
    url(r'^unanswered/$', views.unanswered, name='unanswered'),
    url(r'^all/$', views.all, name='all'),
    url(r'^ask/$', views.AskQuestion.as_view(), name='ask'),
    url(r'^favorite/$', views.favorite, name='favorite'),
    url(r'^answer/$', views.answer, name='answer'),
    url(r'^answer/accept/$', views.accept, name='accept'),
    url(r'^answer/vote/$', views.vote, name='vote'),
    url(r'^question/vote/$', views.question_vote, name='question_vote'),
    url(r'^(\d+)/$', views.question, name='question'),
]
