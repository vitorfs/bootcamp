from django.shortcuts import render
from bootcamp.feeds.views import feeds
from django.contrib.auth.models import User
from bootcamp.feeds.models import Feed
from bootcamp.feeds.views import FEEDS_NUM_PAGES
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        return render(request, 'core/cover.html')

@login_required
def network(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'core/network.html', {'users': users})

@login_required
def profile(request, username):
    page_user = User.objects.get(username=username)
    all_feeds = Feed.get_feeds().filter(user=page_user)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'core/profile.html', {
        'page_user': page_user, 
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1
        })