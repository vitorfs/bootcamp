from django.shortcuts import render
from bootcamp.feeds.models import Feed

def post(request):
    feed = Feed()
    feed.user = request.user
    feed.post = request.POST['post']
    feed.save()
    return render(request, 'feeds/partial_feed.html', {'feed': feed})