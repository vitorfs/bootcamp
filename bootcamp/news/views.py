from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bootcamp.news.models import News


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    success_url = reverse_lazy("news:list")


class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    paginate = 30
