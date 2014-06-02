from django.shortcuts import render
from bootcamp.feeds.views import feeds

def home(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        return render(request, 'core/cover.html')