from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView

from .models import User
from .forms import *
from django.contrib.auth import login

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "account/signup.html"

    def form_valid(self, form):
        # Log the user in upon successful registration
        user = form.save()
        login(self.request, user)
        return redirect("users:detail", username=user.username)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
        "email",
        "picture",
        "job_title",
        "location",
        "personal_url",
        "facebook_account",
        "twitter_account",
        "github_account",
        "linkedin_account",
        "short_bio",
        "bio",
    ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
