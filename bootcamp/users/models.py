from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from allauth.account.forms import ChangePasswordForm
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in, user_logged_out

from bootcamp.notifications.models import Notification, create_notification_handler


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_("User's name"), blank=True, max_length=255)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(_("Location"), max_length=50, null=True, blank=True)
    job_title = models.CharField(_("Job title"), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _("Personal URL"), max_length=555, blank=True, null=True
    )
    bio = models.CharField(_("Short bio"), max_length=280, blank=True, null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='following', blank=True
    )
    contact_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='contacters', blank=True
    )
    pending_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='my_pending_requests', blank=True
    )
    member_since = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.name:
            return self.name

        return self.username

    def get_picture(self):
        default_picture = settings.STATIC_URL + 'img/user.png'
        if self.image:
            return self.image.url
        else:
            return default_picture


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
