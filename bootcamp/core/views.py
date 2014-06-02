from django.shortcuts import render
from bootcamp.feeds.views import feeds
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        return render(request, 'core/cover.html')

def network(request):
    users = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'core/network.html', {'users': users})

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'core/profile.html', {'user': user})