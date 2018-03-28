import json
import uuid

from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.query import QuerySet
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from bootcamp.notifications.signals import notify


class NotificationQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def unread(self, include_deleted=False):
        """Return only unread items in the current queryset"""
        return self.filter(unread=True)

    def read(self, include_deleted=False):
        """Return only read items in the current queryset"""
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset with
        optional filter by recipient first.
        """
        qs = self.unread(True)
        if recipient:
            qs = qs.filter(recipient=recipient)

        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset with
        optional filter by recipient first.
        """
        qs = self.read(True)
        if recipient:
            qs = qs.filter(recipient=recipient)

        return qs.update(unread=True)


class Notification(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    This model is an adaptation from the django package django-notifications at
    https://github.com/django-notifications/django-notifications

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <target> <time>
        <actor> <verb> <action_object> <target> <time>

    Examples::

        <Sebastian> <Logged In> <1 minute ago>
        <Sebastian> <commented> <Article> <2 hours ago>
        <Sebastian> <commented> <comment> on <question> <about 2 hours ago>
    """
    LIKED = 'L'
    COMMENTED = 'C'
    FAVORITED = 'F'
    ANSWERED = 'A'
    ACCEPTED_ANSWER = 'W'
    EDITED_ARTICLE = 'E'
    ALSO_COMMENTED = 'K'
    LOGGED_IN = 'I'
    LOGGED_OUT = 'O'
    UPVOTED = 'U'
    SHARED = 'S'
    NOTIFICATION_TYPES = (
        (LIKED, _('Liked')),
        (COMMENTED, _('Commented')),
        (FAVORITED, _('Favorited')),
        (ANSWERED, _('Answered')),
        (ACCEPTED_ANSWER, _('Accepted')),
        (EDITED_ARTICLE, _('Edited')),
        (ALSO_COMMENTED, _('Also commented')),
        (LOGGED_IN, _('Logged In')),
        (LOGGED_OUT, _('Logged Out')),
        (UPVOTED, _('Up voted')),
        (SHARED, _('Shared')),
        )
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='notify_actor',
                              on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='notifications',
                                  on_delete=models.CASCADE)
    unread = models.BooleanField(default=True, blank=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=210, null=True, blank=True)

    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)

    action_object_content_type = models.ForeignKey(ContentType,
        blank=True, null=True, related_name='notify_action_object',
        on_delete=models.CASCADE)
    action_object_object_id = models.CharField(
        max_length=255, blank=True, null=True)
    action_object = GenericForeignKey(
        'action_object_content_type', 'action_object_object_id')

    target_content_type = models.ForeignKey(ContentType,
        related_name='notify_target', blank=True, null=True,
        on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-timestamp', )
        app_label = 'notifications'

    def __str__(self):
        if self.target:
            if self.action_object:
                return f'{self.actor} {self.verb} {self.action_object} on {self.target} {self.time_since} ago'

            return f'{self.actor} {self.verb} {self.target} {self.time_since} ago'

        if self.action_object:
            return f'{self.actor} {self.verb} {self.action_object} {self.time_since} ago'

        return f'{actor} {verb} {time_since} ago'

    @property
    def time_since(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince


        return timesince(self.timestamp, now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.recipient} {self.uuid_id} {self.verb}',
                                to_lower=True, max_length=200)

        super(Notification, self).save(*args, **kwargs)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def notify_handler(verb, **kwargs):
    """
    Handler function to create a Notification instance upon action signal call.
    """
    # Pull the options out of kwargs
    kwargs.pop('signal', None)
    recipient = kwargs.pop('recipient')
    actor = kwargs.pop('sender')
    optional_objs = [
        (kwargs.pop(opt, None), opt)
        for opt in ('target', 'action_object')
    ]

    # Check if User or Group
    if isinstance(recipient, Group):
        recipients = recipient.user_set.all()

    elif isinstance(recipient, QuerySet) or isinstance(recipient, list):
        recipients = recipient

    else:
        recipients = [recipient]

    new_notifications = []

    for recipient in recipients:
        newnotify = Notification(
            recipient=recipient,
            actor_content_type=ContentType.objects.get_for_model(actor),
            actor_object_id=actor.pk,
            verb=text_type(verb)
        )

        # Set optional objects
        for obj, opt in optional_objs:
            if obj is not None:
                setattr(newnotify, '%s_object_id' % opt, obj.pk)
                setattr(newnotify, '%s_content_type' % opt,
                        ContentType.objects.get_for_model(obj))

        if len(kwargs) and EXTRA_DATA:
            newnotify.data = kwargs

        newnotify.save()
        new_notifications.append(newnotify)

    return new_notifications


# connect the signal
notify.connect(notify_handler)
