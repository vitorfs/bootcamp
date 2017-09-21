import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden)
from django.shortcuts import get_object_or_404, render
from django.template.context_processors import csrf
from django.template.loader import render_to_string

from bootcamp.activities.models import Activity
from bootcamp.decorators import ajax_required
from bootcamp.feeds.models import Feed

FEEDS_NUM_PAGES = 10


@login_required
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


def feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
@ajax_required
def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    feed_source = request.GET.get('feed_source')
    all_feeds = Feed.get_feeds(from_feed)
    if feed_source != 'all':
        all_feeds = all_feeds.filter(user__id=feed_source)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
    html = ''
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string('feeds/partial_feed.html',
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token
                                                    }))

    return HttpResponse(html)


def _html_feeds(last_feed, user, csrf_token, feed_source='all'):
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    html = ''
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string('feeds/partial_feed.html',
                                                {
                                                    'feed': feed,
                                                    'user': user,
                                                    'csrf_token': csrf_token
                                                    }))

    return html


@login_required
@ajax_required
def load_new(request):
    last_feed = request.GET.get('last_feed')
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)


@login_required
@ajax_required
def check(request):
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds_after(last_feed)
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)

    count = feeds.count()
    return HttpResponse(count)


@login_required
@ajax_required
def post(request):
    last_feed = request.POST.get('last_feed')
    user = request.user
    csrf_token = (csrf(request)['csrf_token'])
    feed = Feed()
    feed.user = user
    post = request.POST['post']
    post = post.strip()
    if len(post) > 0:
        feed.post = post[:255]
        feed.save()
    html = _html_feeds(last_feed, user, csrf_token)
    return HttpResponse(html)


@login_required
@ajax_required
def like(request):
    feed_id = request.POST['feed']
    feed = Feed.objects.get(pk=feed_id)
    user = request.user
    like = Activity.objects.filter(activity_type=Activity.LIKE, feed=feed_id,
                                   user=user)
    if like:
        user.profile.unotify_liked(feed)
        like.delete()

    else:
        like = Activity(activity_type=Activity.LIKE, feed=feed_id, user=user)
        like.save()
        user.profile.notify_liked(feed)

    return HttpResponse(feed.calculate_likes())


@login_required
@ajax_required
def comment(request):
    if request.method == 'POST':
        feed_id = request.POST['feed']
        feed = Feed.objects.get(pk=feed_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:255]
            user = request.user
            feed.comment(user=user, post=post)
            user.profile.notify_commented(feed)
            user.profile.notify_also_commented(feed)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})

    else:
        feed_id = request.GET.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        return render(request, 'feeds/partial_feed_comments.html',
                      {'feed': feed})


@login_required
@ajax_required
def update(request):
    first_feed = request.GET.get('first_feed')
    last_feed = request.GET.get('last_feed')
    feed_source = request.GET.get('feed_source')
    feeds = Feed.get_feeds().filter(id__range=(last_feed, first_feed))
    if feed_source != 'all':
        feeds = feeds.filter(user__id=feed_source)
    dump = {}
    for feed in feeds:
        dump[feed.pk] = {'likes': feed.likes, 'comments': feed.comments}
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')


@login_required
@ajax_required
def track_comments(request):
    feed_id = request.GET.get('feed')
    feed = Feed.objects.get(pk=feed_id)
    if len(feed.get_comments()) > 0:
        return render(
            request, 'feeds/partial_feed_comments.html', {'feed': feed})

    else:
        return HttpResponse()


@login_required
@ajax_required
def remove(request):
    try:
        feed_id = request.POST.get('feed')
        feed = Feed.objects.get(pk=feed_id)
        if feed.user == request.user:
            likes = feed.get_likes()
            parent = feed.parent
            for like in likes:
                like.delete()
            feed.delete()
            if parent:
                parent.calculate_comments()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()
