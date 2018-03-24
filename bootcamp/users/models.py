from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    picture = models.ImageField(
        _('Profile Picture'), upload_to='profile_pics/', null=True, blank=True)
    location = models.CharField(
        _('Location'), max_length=50, null=True, blank=True)
    job_title = models.CharField(
        _('Job Title'), max_length=50, null=True, blank=True)
    personal_url = models.URLField(
        _('Personal URL'), max_length=555, blank=True, null=True)
    facebook_account = models.URLField(
        _('Facebook Profile'), max_length=255, blank=True, null=True)
    twitter_account = models.URLField(
        _('Twitter Account'), max_length=255, blank=True, null=True)
    github_account = models.URLField(
        _('GitHub Profile'), max_length=255, blank=True, null=True)
    linkedin_account = models.URLField(
        _('LinkedIn Profile'), max_length=255, blank=True, null=True)
    short_bio = models.CharField(
        _('Describe Yourself'), max_length=60, blank=True, null=True)
    bio = models.CharField(
        _('Short bio'), max_length=280, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
