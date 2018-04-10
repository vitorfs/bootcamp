from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from bootcamp.mixins import AuthorRequiredMixin
from bootcamp.articles.models import Article


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
        return Article.get_published()

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
        return Article.get_drafts()


class CreateArticleView(LoginRequiredMixin, CreateView):
    """Basic CreateView implementation to create new articles."""
    message = _("Your article has been created.")
    fields = ["title", "content", "image", "tags"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateArticle, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('articles:list')


class EditArticleView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Basic EditView implementation to edit existing articles."""
    model = Article
    message = _("Your article has been updated.")

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('articles:list')


class DetailArticleView(LoginRequiredMixin, DetailView):
    """Basic DetailView implementation to call an individual article."""
    model = Article
