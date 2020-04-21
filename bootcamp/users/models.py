import hashlib
import os.path
import urllib
from django.contrib.auth.models import AbstractUser
from allauth.account.forms import ChangePasswordForm
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out

from bootcamp.notifications.models import Notification, create_notification_handler


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_("User's name"), blank=True, max_length=255)
    location = models.CharField(_("Location"), max_length=50, null=True, blank=True)
    job_title = models.CharField(_("Job title"), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _("Personal URL"), max_length=555, blank=True, null=True
    )
    facebook_account = models.URLField(
        _("Facebook profile"), max_length=255, blank=True, null=True
    )
    twitter_account = models.URLField(
        _("Twitter account"), max_length=255, blank=True, null=True
    )
    github_account = models.URLField(
        _("GitHub profile"), max_length=255, blank=True, null=True
    )
    linkedin_account = models.URLField(
        _("LinkedIn profile"), max_length=255, blank=True, null=True
    )
    short_bio = models.CharField(
        _("Describe yourself"), max_length=60, blank=True, null=True
    )
    bio = models.CharField(_("Short bio"), max_length=280, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username

    def get_picture(self):
        no_picture = "http://trybootcamp.vitorfs.com/static/img/user.png"
        try:
            filename = settings.MEDIA_ROOT + "/profile_pics/" + self.username + ".jpg"
            picture_url = settings.MEDIA_URL + "profile_pics/" + self.username + ".jpg"
            if os.path.isfile(filename):  # pragma: no cover
                return picture_url
            else:  # pragma: no cover
                gravatar_url = "http://www.gravatar.com/avatar/{0}?{1}".format(
                    hashlib.md5(self.email.lower()).hexdigest(),
                    urllib.urlencode({"d": no_picture, "s": "256"}),
                )
                return gravatar_url

        except Exception:
            return no_picture


class CustomChangePasswordForm(ChangePasswordForm):
    def save(self):
        super(CustomChangePasswordForm, self).save()
        # Add your own processing here.


def broadcast_login(sender, user, request, **kwargs):
    """Handler to be fired up upon user login signal to notify all users."""
    create_notification_handler(user, "global", Notification.LOGGED_IN)


def broadcast_logout(sender, user, request, **kwargs):
    """Handler to be fired up upon user logout signal to notify all users."""
    create_notification_handler(user, "global", Notification.LOGGED_OUT)


# user_logged_in.connect(broadcast_login)
# user_logged_out.connect(broadcast_logout)
