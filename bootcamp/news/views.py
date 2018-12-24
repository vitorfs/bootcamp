from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView

from bootcamp.helpers import ajax_required, AuthorRequiredMixin
from bootcamp.news.models import News


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
@require_http_methods(["POST"])
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
            'news/news_single.html',
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
@require_http_methods(["POST"])
def like(request):
    """Function view to receive AJAX, returns the count of likes a given news
    has recieved."""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    user = request.user
    news.switch_like(user)
    return JsonResponse({"likes": news.count_likers()})


@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """Returns a list of news with the given news as parent."""
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    news_html = render_to_string("news/news_single.html", {"news": news})
    thread_html = render_to_string(
        "news/news_thread.html", {"thread": news.get_thread()})
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """A function view to implement the post functionality with AJAX, creating
    News instances who happens to be the children and commenters of the root
    post."""
    user = request.user
    post = request.POST['reply']
    par = request.POST['parent']
    parent = News.objects.get(pk=par)
    post = post.strip()
    if post:
        parent.reply_this(user, post)
        return JsonResponse({'comments': parent.count_thread()})

    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    data = {'likes': news.count_likers(), 'comments': news.count_thread()}
    return JsonResponse(data)
