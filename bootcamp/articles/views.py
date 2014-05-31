from django.shortcuts import render, redirect
from bootcamp.articles.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.articles.forms import ArticleForm

def articles(request):
    all_articles = Article.get_published()
    paginator = Paginator(all_articles, 10)

    if 'page' not in request.GET:
        page = 1
    else:
        page = request.GET.get('page')

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    page_loop_times = [i+1 for i in range(paginator.num_pages)]

    return render(request, 'articles/articles.html', {
        'articles': articles,
        'page': page,
        'num_pages': paginator.num_pages,
        'page_loop_times': page_loop_times
        })

def write(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.create_user = request.user
            article.title = form.cleaned_data.get('title')
            article.content = form.cleaned_data.get('content')
            article.tags = form.cleaned_data.get('tags')
            status = form.cleaned_data.get('status')
            if status in [Article.PUBLISHED, Article.DRAFT]:
                article.status = form.cleaned_data.get('status')
            article.save()
            return redirect('/articles/')
    else:
        form = ArticleForm()
    return render(request, 'articles/write.html', {'form': form})

def drafts(request):
    return render(request, 'articles/articles.html')