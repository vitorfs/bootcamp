from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from bootcamp.feeds.models import Feed
from bootcamp.activities.models import Activity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from django.utils import simplejson

FEEDS_NUM_PAGES = 10

def feeds(request):
    all_feeds = Feed.get_feeds()
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'feeds/feeds.html', {
        'feeds': feeds, 
        'from_feed': from_feed, 
        'page': 1,
        })

def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    all_feeds = Feed.get_feeds(from_feed)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
    html = u''
    csrf_token = unicode(csrf(request)['csrf_token'])
    for feed in feeds:
        html = u'{0}{1}'.format(html, render_to_string('feeds/partial_feed.html', {
            'feed': feed,
            'user': request.user,
            'csrf_token': csrf_token
            })
        )
    return HttpResponse(html)

def _html_feeds(last_feed, user, csrf_token):
    feeds = Feed.get_feeds_after(last_feed)
    html = u''
    for feed in feeds:
        html = u'{0}{1}'.format(html, render_to_string('feeds/partial_feed.html', {
            'feed': feed,
            'user': user,
            'csrf_token': csrf_token
            })
        )
    return html

def load_new(request):
    last_feed = request.GET.get('last_feed')
    user = request.user
    csrf_token = unicode(csrf(request)['csrf_token'])
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)

def check(request):
    last_feed = request.GET.get('last_feed')
    count = Feed.get_feeds_after(last_feed).count()
    return HttpResponse(count)

def post(request):
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = unicode(csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    feed.post = request.POST['post']
    feed.save()
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)

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

def comment(request):
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        user = request.user
        feed.do_comment(user=user, post=post)
        return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})
    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html', {'feed': feed})

def update(request):
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments}
    data = simplejson.dumps(dump)
    return HttpResponse(data, mimetype='application/json')