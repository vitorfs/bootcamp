from django.conf.urls import include, url

from bootcamp.qa import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.QuestionListView.as_view(), name='index'),
    url(r'^question-detail/(?P<slug>[-_\w]+)/$',
        views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^answer-detail/(?P<uuid_id>\d+)/$',
        views.AnswerDetailView.as_view(), name='answer_detail'),
    url(r'^ask-question/$', views.CreateQuestionView.as_view(),
        name='ask_question'),
    url(r'^propose-answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='propose_answer'),
]
