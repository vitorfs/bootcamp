import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from bootcamp.news.models import News
from bootcamp.mixins import ajax_required


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    paginate_by = 15


@login_required
@ajax_required
def post(request):
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0 and len(post) <= 280:
        posted = News.objects.create(
            user=user,
            content=post,
        )
        html = render_to_string(
            'news/partial_news.html',
            {
                'news': posted,
                'csrf_token': csrf_token,
                'request': request
            })
        return HttpResponse(html)

    else:
        return HttpResponseBadRequest()
