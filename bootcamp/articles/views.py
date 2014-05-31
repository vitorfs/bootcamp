from django.shortcuts import render
from bootcamp.articles.models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    return render(request, 'articles/articles.html')

def drafts(request):
    return render(request, 'articles/articles.html')