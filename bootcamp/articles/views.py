from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from bootcamp.articles.models import Article, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bootcamp.articles.forms import ArticleForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

class ArticlesList(ListView):
    model = Article
    queryset = Article.get_published()
    paginate_by = 25
    context_object_name = 'articles'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesList, self).get_context_data(*args, **kwargs)
        context.update({'popular_tags': Tag.get_popular_tags()})
        return context

class ArticleView(DetailView):
    model = Article
    context_obj_name = 'article'

class ArticleCreateView(FormView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_form.html'
    success_url = '/articles/'

    def post(self, request):
        form = ArticleForm(request.POST, request.FILES)
        a = request.POST.get('action').lower()
        if form.is_valid():
            if a == 'publish':
                status = Article.PUBLISHED
            elif a == 'save draft':
                status = Article.DRAFT
            article = Article(
                title = form.cleaned_data.get('title'),
                content = form.cleaned_data.get('content'),
                create_user = request.user,
                status = status
            )
            article.save()
            tags = form.cleaned_data.get('tags')
            article.create_tags(tags)
            return redirect(self.success_url)
        else:
            return super(ArticleCreateView, self).form_invalid(form) 


class ArticleTagView(ArticlesList):
    model = Tag
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        queryset = Tag.objects.filter(article__status = Article.PUBLISHED, 
                                      tag = self.kwargs.get('tag_name'))
        return [t.article for t in queryset]
    

class ArticlesDraftListView(ArticlesList):
    context_object_name = 'drafts'
    template_name  = 'articles/drafts.html' 

    def get_queryset(self):
        return Article.objects.filter(create_user = self.request.user,
                                      status = Article.DRAFT)

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
