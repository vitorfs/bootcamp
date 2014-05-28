from django.shortcuts import render
from bootcamp.feeds.models import Feed

def home(request):
    feeds = Feed.objects.all()
    return render(request, 'core/home.html', {'feeds': feeds})