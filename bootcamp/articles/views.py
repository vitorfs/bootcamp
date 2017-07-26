from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

import markdown
from bootcamp.articles.forms import ArticleForm
from bootcamp.articles.models import Article, ArticleComment
from bootcamp.decorators import ajax_required


def _articles(request, articles):
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)

    except PageNotAnInteger:
        articles = paginator.page(1)

    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    popular_tags = Article.get_counted_tags()

    return render(request, 'articles/articles.html', {
        'articles': articles,
        'popular_tags': popular_tags
    })


class CreateArticle(LoginRequiredMixin, CreateView):
    """
    """
    template_name = 'articles/write.html'
    form_class = ArticleForm
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        return super(CreateArticle, self).form_valid(form)


@login_required
def articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)


@login_required
def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'articles/article.html', {'article': article})


@login_required
def tag(request, tag_name):
    articles = Article.objects.filter(tags__name=tag_name).filter(status='P')
    return _articles(request, articles)


@login_required
def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.create_user = request.user
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            status = form.cleaned_data.get('status')
            if status in [Article.PUBLISHED, Article.DRAFT]:
                article.status = form.cleaned_data.get('status')
            article.save()
            tags = form.cleaned_data.get('tags')
            article.create_tags(tags)
            return redirect('/articles/')
    else:
        form = ArticleForm()
    return render(request, 'articles/write.html', {'form': form})


@login_required
def drafts(request):
    drafts = Article.objects.filter(create_user=request.user,
                                    status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})


@login_required
def edit(request, id):
    tags = ''
    if id:
        article = get_object_or_404(Article, pk=id)
        for tag in article.get_tags():
            tags = '{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        article = Article(create_user=request.user)

    if article.create_user.id != request.user.id:
        return redirect('home')

    if request.POST:
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/articles/')
    else:
        form = ArticleForm(instance=article, initial={'tags': tags})
    return render(request, 'articles/edit.html', {'form': form})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                html = markdown.markdown(content, safe_mode='escape')
            return HttpResponse(html)
        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            article_id = request.POST.get('article')
            article = Article.objects.get(pk=article_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                article_comment = ArticleComment(user=request.user,
                                                 article=article,
                                                 comment=comment)
                article_comment.save()
            html = ''
            for comment in article.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'articles/partial_article_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()
