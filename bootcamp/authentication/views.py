from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from bootcamp.authentication.forms import SignUpForm
from bootcamp.feeds.models import Feed


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'authentication/signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            welcome_post = '{0} has joined the network.'.format(user.username,
                                                                user.username)
            feed = Feed(user=user, post=welcome_post)
            feed.save()
            return redirect('/')

    else:
        return render(request, 'authentication/signup.html',
                      {'form': SignUpForm()})
