from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.questions.views',
    url(r'^$', 'questions', name='questions'),
    url(r'^answered/$', 'answered', name='answered'),
    url(r'^unanswered/$', 'unanswered', name='unanswered'),
    url(r'^all/$', 'all', name='all'),
    url(r'^ask/$', 'ask', name='ask'),
    url(r'^favorite/$', 'favorite', name='favorite'),
    url(r'^answer/$', 'answer', name='answer'),
    url(r'^answer/accept/$', 'accept', name='accept'),
    url(r'^answer/vote/$', 'vote', name='vote'),
    url(r'^(\d+)/$', 'question', name='question'),
)