from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from bootcamp.feeds.views import feeds
from django.contrib import messages

def login(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    else:
                        return redirect('/')
                else:
                    messages.add_message(request, messages.ERROR, 'Your account is desactivated.')
                    return render(request, 'core/cover.html')
            else:
                messages.add_message(request, messages.ERROR, 'Username or password invalid.')
                return render(request, 'core/cover.html')
        else:
            return render(request, 'core/cover.html')

def logout(request):
    django_logout(request)
    return redirect('/')

def signup(request):
    pass