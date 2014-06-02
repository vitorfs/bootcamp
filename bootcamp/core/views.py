from django.shortcuts import render
from bootcamp.feeds.views import feeds
from django.contrib.auth.models import User
from bootcamp.feeds.models import Feed
from bootcamp.feeds.views import FEEDS_NUM_PAGES
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from bootcamp.core.forms import ProfileForm, ChangePasswordForm
from django.contrib import messages

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

@login_required
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile were successfully edited.')
    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location
            })
    return render(request, 'core/settings.html', {'form':form})

@login_required
def password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your password were successfully changed.')
    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'core/password.html', {'form':form})