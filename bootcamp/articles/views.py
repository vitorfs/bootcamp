from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from bootcamp.articles.models import Article, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.articles.forms import ArticleForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

class ArticlesList(ListView):
    model = Article
    queryset = Article.get_published()
    paginate_by = 1
    context_object_name = 'articles'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesList, self).get_context_data(*args, **kwargs)
        context.update({'popular_tags': Tag.get_popular_tags()})
        return context

@login_required
def articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)

@login_required
def article(request, slug):
    try:
        article = Article.objects.get(slug=slug, status=Article.PUBLISHED)
        return render(request, 'articles/article.html', {'article': article})
    except Article.DoesNotExist:
        return redirect('/articles/')

@login_required
def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    articles = []
    for tag in tags:
        if tag.article.status == Article.PUBLISHED:
            articles.append(tag.article)
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
    drafts = Article.objects.filter(create_user=request.user, status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})

@login_required
def edit(request, id):
    tags = ''
    if id:
        article = get_object_or_404(Article, pk=id)
        for tag in article.get_tags():
            tags = u'{0} {1}'.format(tags, tag.tag)
        tags = tags.strip()
    else:
        article = Article(create_user=request.user)

    if request.POST:
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/articles/')
    else:
        form = ArticleForm(instance=article, initial={'tags': tags})
    return render(request, 'articles/edit.html', {'form': form})
