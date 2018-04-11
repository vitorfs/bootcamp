from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootcamp.mixins import AuthorRequiredMixin
from bootcamp.articles.models import Article
from bootcamp.articles.forms import ArticleForm


class ArticlesListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the published articles list."""
    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_context_data(self, *args, **kwargs):
        context = super(
            ArticlesListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.get_published()

class DraftsListView(LoginRequiredMixin, ListView):
    """Basic ListView implementation to call the drafts articles list."""
    model = Article
    paginate_by = 15
    context_object_name = "articles"

    def get_context_data(self, *args, **kwargs):
        context = super(
            DraftsListView, self).get_context_data(*args, **kwargs)
        context['popular_tags'] = Article.get_counted_tags()
        return context

    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()


class CreateArticleView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""
    model = Article
    message = _("Your article has been created.")
    form_class = ArticleForm
    template_name = 'articles/article_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateArticleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('articles:list')


class EditArticleView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing articles."""
    model = Article
    message = _("Your article has been updated.")
    form_class = ArticleForm
    template_name = 'articles/article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EditArticleView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('articles:list')


class DetailArticleView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual article."""
    model = Article
