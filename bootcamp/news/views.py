from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView

from bootcamp.news.models import News
from bootcamp.mixins import ajax_required, AuthorRequiredMixin


class NewsListView(LoginRequiredMixin, ListView):
    """A really simple ListView, with some JS magic on the UI."""
    model = News
    paginate_by = 15

    def get_queryset(self, **kwargs):
        return News.objects.filter(reply=False)


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Implementation of the DeleteView overriding the delete method to
    allow a no-redirect response to use with AJAX call."""
    model = News
    success_url = reverse_lazy("news:list")


@login_required
@ajax_required
def post_news(request):
    """A function view to implement the post functionality with AJAX allowing
    to create News instances as parent ones."""
    user = request.user
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
                'request': request
            })
        return HttpResponse(html)

    else:
        lenght = len(post) - 280
        return HttpResponseBadRequest(
            content=_(f'Text is {lenght} characters longer than accepted.'))


@login_required
@ajax_required
def like(request):
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    user = request.user
    news.switch_like(user)
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
def get_news_comments(request):
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id).get_thread()
    return render(request,
                  'news/news_comments.html',
                  {'news_list': news}
                  )


@login_required
@ajax_required
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    News instances who happens to be the children and commenters of the root
    post."""
    user = request.user
    post = request.POST['post']
    par = request.POST['parent']
    parent = News.objects.get(pk=par)
    news = parent.get_thread()
    post = post.strip()
    if post:
        posted = News.objects.create(
            user=user,
            content=post,
            reply=True,
            parent=parent
        )
        return JsonResponse({'comments': parent.count_thread()})

    else:
        return HttpResponseBadRequest()
