from django.shortcuts import render
from bootcamp.feeds.models import Feed

def feeds(request):
    feeds = Feed.objects.all()
    return render(request, 'feeds/feeds.html', {'feeds': feeds})

def post(request):
    feed = Feed()
    feed.user = request.user
    feed.post = request.POST['post']
    feed.save()
    return render(request, 'feeds/partial_feed.html', {'feed': feed})