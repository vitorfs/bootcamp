from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from bootcamp.articles.models import Article, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.articles.forms import ArticleForm
from django.shortcuts import get_object_or_404

def _articles(request, articles):
    paginator = Paginator(articles, 10)
    if 'page' not in request.GET:
        page = 1
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    page_loop_times = [i+1 for i in range(paginator.num_pages)]
    popular_tags = Tag.get_popular_tags()
    return render(request, 'articles/articles.html', {
        'articles': articles,
        'page': page,
        'num_pages': paginator.num_pages,
        'page_loop_times': page_loop_times,
        'popular_tags': popular_tags
        })    

def articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)

def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    articles = []
    for tag in tags:
        if tag.article.status == Article.PUBLISHED:
            articles.append(tag.article)
    return _articles(request, articles)

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

def drafts(request):
    drafts = Article.objects.filter(create_user=request.user, status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})

def edit(request, id):
    if id:
        article = get_object_or_404(Article, pk=id)
        tags = ''
        for tag in article.get_tags():
            tags = u'{0} {1}'.format(tags, tag.tag)
        article.tags = tags.strip()
    else:
        article = Article(create_user=request.user)

    if request.POST:
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('/articles/')
    else:
        form = ArticleForm(instance=article)
        return render(request, 'articles/edit.html', {'form': form})