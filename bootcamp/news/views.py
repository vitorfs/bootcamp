from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from bootcamp.news.models import News


class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    success_url = reverse_lazy("news:list")


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = News


class TweetListView(LoginRequiredMixin, ListView):
    model = News
