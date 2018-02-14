from __future__ import unicode_literals

import json
import hashlib
import os.path
import urllib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth import user_logged_in, user_logged_out


from channels import Group

from bootcamp.activities.models import Notification


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username

    def get_url(self):
        url = self.url
        if "http://" not in self.url and "https://" not in self.url and len(self.url) > 0:  # noqa: E501
            url = "http://" + str(self.url)

        return url

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):  # pragma: no cover
                return picture_url
            else:  # pragma: no cover
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()

            else:
                return self.user.username

        except Exception:  # pragma: no cover
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

        self.group_notification('liked')
        feed.feed_log('liked')

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

        self.group_notification('commented')
        feed.feed_log('commented')

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

        self.group_notification('favorited')

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

        self.group_notification('answered')

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

        self.group_notification('accepted_answer')

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()

    def notify_login(self):
        Notification.objects.filter(
            notification_type=Notification.LOGGED_OUT, from_user=self.user,
            to_user=self.user).delete()
        Notification.objects.get_or_create(
            notification_type=Notification.LOGGED_IN, from_user=self.user,
            to_user=self.user)
        self.group_notification('log in')

    def notify_logout(self):
        Notification.objects.filter(
            notification_type=Notification.LOGGED_IN, from_user=self.user,
            to_user=self.user).delete()
        Notification.objects.get_or_create(
            notification_type=Notification.LOGGED_OUT, from_user=self.user,
            to_user=self.user)
        self.group_notification('log out')

    def notify_upvoted_question(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.UPVOTED_Q,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

        self.group_notification('upvoted_question')

    def notify_upvoted_answer(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.UPVOTED_A,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

        self.group_notification('upvoted_answer')

    def group_notification(self, activity):
        Group('notifications').send({
            'text': json.dumps({
                'username': self.user.username,
                'activity_type': 'notification',
                'activity': activity
            })
        })


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def on_user_login(sender, **kwargs):
    Profile.objects.get(user=kwargs['user']).notify_login()


def on_user_logout(sender, **kwargs):
    Profile.objects.get(user=kwargs['user']).notify_logout()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
user_logged_in.connect(on_user_login, sender=User)
user_logged_out.connect(on_user_logout, sender=User)
