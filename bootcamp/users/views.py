import os
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.conf import settings as django_settings
from .models import User
from ..news.models import News


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    paginate_by = 20
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_activity'] = News.objects.filter(user=context['user'])
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
        "email",
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


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get("upload_picture") == "uploaded":
            uploaded_picture = True

    except Exception:  # pragma: no cover
        pass

    return render(
        request, "users/user_picture.html", {"uploaded_picture": uploaded_picture}
    )


@login_required
def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + "/profile_pics/"
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)

        f = request.FILES["picture"]
        filename = profile_pictures + request.user.username + "_tmp.jpg"
        with open(filename, "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect("/picture/?upload_picture=uploaded")

    except Exception:
        return redirect("/picture/")


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
        w = int(request.POST.get("w"))
        h = int(request.POST.get("h"))
        tmp_filename = (
            django_settings.MEDIA_ROOT
            + "/profile_pics/"
            + request.user.username
            + "_tmp.jpg"
        )
        filename = (
            django_settings.MEDIA_ROOT
            + "/profile_pics/"
            + request.user.username
            + ".jpg"
        )
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect("/picture/")
