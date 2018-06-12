from django.conf.urls import include, url

from bootcamp.qa import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.QuestionListView.as_view(), name='index'),
    url(r'^question-detail/(?P<pk>\d+)/$',
        views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^ask-question/$', views.CreateQuestionView.as_view(),
        name='ask_question'),
    url(r'^propose-answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='propose_answer'),
    url(r'^question/vote/$', views.question_vote, name='question_vote'),
]
