from django.conf.urls import include, url

from bootcamp.qa import views

urlpatterns = [
    url(r'^$', views.QuestionListView.as_view(), name='index'),
    url(r'^question-detail/(?P<slug>[-_\w]+)/$',
        views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^answer-detail/(?P<uuid_id>\d+)/$',
        views.AnswerDetailView.as_view(), name='answer_detail'),
    url(r'^new-question/$', views.CreateQuestionView.as_view(),
        name='create_question'),
    url(r'^create-answer/(?P<question_id>\d+)/$',
        views.CreateAnswerView.as_view(), name='create_answer'),
]
