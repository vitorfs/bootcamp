from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from bootcamp.feeds.views import feeds
from django.contrib import messages
from bootcamp.auth.forms import SignUpForm
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'auth/signup.html', {'form': form})
        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            django_login(request, user)
            return feeds(request)
    else:
        return render(request, 'auth/signup.html', {'form': SignUpForm()})
