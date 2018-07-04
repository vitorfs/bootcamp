from django.conf.urls import url

from bootcamp.qa import views

app_name = 'qa'
urlpatterns = [
    url(r'^$', views.QuestionListView.as_view(), name='index_noans'),
    url(r'^answered/$', views.QuestionAnsListView.as_view(), name='index_ans'),
    url(r'^indexed/$', views.QuestionsIndexListView.as_view(), name='index_all'),
    url(r'^question-detail/(?P<pk>\d+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^ask-question/$', views.CreateQuestionView.as_view(), name='ask_question'),
    url(r'^propose-answer/(?P<question_id>\d+)/$', views.CreateAnswerView.as_view(), name='propose_answer'),
    url(r'^question/vote/$', views.question_vote, name='question_vote'),
    url(r'^answer/vote/$', views.answer_vote, name='answer_vote'),
    url(r'^accept-answer/$', views.accept_answer, name='accept_answer'),
]
