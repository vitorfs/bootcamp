from django.shortcuts import render
from django.http import HttpResponse
from bootcamp.feeds.models import Feed
from bootcamp.activities.models import Activity

def feeds(request):
    feeds = Feed.objects.all()
    return render(request, 'feeds/feeds.html', {'feeds': feeds})

def post(request):
    feed = Feed()
    feed.user = request.user
    feed.post = request.POST['post']
    feed.save()
    return render(request, 'feeds/partial_feed.html', {'feed': feed})

def like(request):
    feed_id = request.POST['feed']
    feed = Feed.objects.get(pk=feed_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id, user=user)
    if like:
        like.delete()
    else:
        like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
        like.save()
    return HttpResponse(feed.calculate_likes())