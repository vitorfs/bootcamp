import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from slugify import slugify


class NotificationQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def unread(self):
        """Return only unread items in the current queryset"""
        return self.filter(unread=True)

    def read(self):
        """Return only read items in the current queryset"""
        return self.filter(unread=False)

    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread elements in the current queryset with
        optional filter by recipient first.
        """
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)

        return qs.update(unread=False)

    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read elements in the current queryset with
        optional filter by recipient first.
        """
        qs = self.read()
        if recipient:
            qs = qs.filter(recipient=recipient)

        return qs.update(unread=True)

    def get_most_recent(self):
        """Returns the most recent unread elements in the queryset"""
        return self.unread()[:5]


class Notification(models.Model):
    """
    Action model describing the actor acting out a verb (on an optional target).
    Nomenclature based on http://activitystrea.ms/specs/atom/1.0/

    This model is an adaptation from the django package django-notifications at
    https://github.com/django-notifications/django-notifications

    Generalized Format::

        <actor> <verb> <time>
        <actor> <verb> <action_object> <time>

    Examples::

        <Sebastian> <Logged In> <1 minute ago>
        <Sebastian> <commented> <Article> <2 hours ago>
    """

    LIKED = "L"
    COMMENTED = "C"
    FAVORITED = "F"
    ANSWERED = "A"
    ACCEPTED_ANSWER = "W"
    EDITED_ARTICLE = "E"
    ALSO_COMMENTED = "K"
    LOGGED_IN = "I"
    LOGGED_OUT = "O"
    VOTED = "V"
    SHARED = "S"
    SIGNUP = "U"
    REPLY = "R"
    FOLLOW = "X"
    FRIEND_REQUEST = "Y"
    FRIEND_ACCEPT = "Z"
    NOTIFICATION_TYPES = (
        (LIKED, _("liked")),
        (COMMENTED, _("commented")),
        (FAVORITED, _("favorited")),
        (ANSWERED, _("answered")),
        (ACCEPTED_ANSWER, _("accepted")),
        (EDITED_ARTICLE, _("edited")),
        (ALSO_COMMENTED, _("also commented")),
        (LOGGED_IN, _("logged in")),
        (LOGGED_OUT, _("logged out")),
        (VOTED, _("voted on")),
        (SHARED, _("shared")),
        (SIGNUP, _("created an account")),
        (FOLLOW, _("followed you")),
        (FRIEND_REQUEST, _("sent you a friend request")),
        (FRIEND_ACCEPT, _("accepted your friend request")),
    )
    _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/news/{3}/">{4}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/news/{3}/">{4}</a>'  # noqa: E501
    _FAVORITED_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/qa/{3}/">{4}</a>'  # noqa: E501
    _ANSWERED_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/qa/{3}/">{4}</a>'  # noqa: E501
    _ACCEPTED_ANSWER_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/qa/{3}/">{4}</a>'  # noqa: E501
    _UPVOTED_QUESTION_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/qa/{3}/">{4}</a>'  # noqa: E501
    _UPVOTED_ANSWER_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/qa/{3}/">{4}</a>'  # noqa: E501
    _EDITED_ARTICLE_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/articles/{3}/">{4}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> {2} <a href="/news/{3}/">{4}</a>'  # noqa: E501
    _FOLLOWED_TEMPLATE = '<a href="/{0}/">{1}</a> {2}.'  # noqa: E501
    _FRIEND_REQUEST_TEMPLATE = '<a href="/{0}/">{1}</a> {2}.'  # noqa: E501
    _FRIEND_ACCEPT_TEMPLATE = '<a href="/{0}/">{1}</a> {2}.'  # noqa: E501
    _USER_LOGIN_TEMPLATE = '<a href="/{0}/">{1}</a> has just logged in.'  # noqa: E501
    _USER_LOGOUT_TEMPLATE = '<a href="/{0}/">{1}</a> has just logged out.'  # noqa: E501

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notify_actor", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    unread = models.BooleanField(default=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=210, null=True, blank=True)
    verb = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    action_object_content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="notify_action_object",
        on_delete=models.CASCADE,
    )
    action_object_object_id = models.CharField(max_length=50, blank=True, null=True)
    action_object = GenericForeignKey(
        "action_object_content_type", "action_object_object_id"
    )
    objects = NotificationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-timestamp",)

    def __str__(self):
        if self.action_object:
            if self.verb == self.LIKED:
                return self._LIKED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.REPLY:
                return self._COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.COMMENTED:
                return self._COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.FAVORITED:
                return self._FAVORITED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.ANSWERED:
                return self._ANSWERED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.ACCEPTED_ANSWER:
                return self._ACCEPTED_ANSWER_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.EDITED_ARTICLE:
                return self._EDITED_ARTICLE_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.ALSO_COMMENTED:
                return self._ALSO_COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object.content))
                )

            elif self.verb == self.FOLLOW:
                return self._ALSO_COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                )

            elif self.verb == self.FRIEND_REQUEST:
                return self._ALSO_COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                )

            elif self.verb == self.FRIEND_ACCEPT:
                return self._ALSO_COMMENTED_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                )

            elif self.verb == self.LOGGED_IN:
                return self._USER_LOGIN_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor)
                )

            elif self.verb == self.LOGGED_OUT:
                return self._USER_LOGOUT_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor)
                )

            elif self.verb == self.VOTED:
                return self._UPVOTED_QUESTION_TEMPLATE.format(
                    escape(self.actor),
                    escape(self.actor),
                    escape(self.get_verb_display()),
                    self.action_object_object_id,
                    escape(self.get_summary(self.action_object))
                )

            else:
                return 'Ooops! Something went wrong.'
        else:
            return f"{self.actor} {self.get_verb_display()} {self.time_since()} ago"

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return '{0}...'.format(value[:summary_size])

        else:
            return value

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.recipient} {self.uuid_id} {self.verb}",
                lowercase=True,
                max_length=200,
            )

        super().save(*args, **kwargs)

    def time_since(self, now=None):
        """
        Shortcut for the ``django.utils.timesince.timesince`` function of the
        current timestamp.
        """
        from django.utils.timesince import timesince

        return timesince(self.timestamp, now)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()


def create_notification_handler(actor, recipient, verb, **kwargs):
    """
    Handler function to create a Notification instance.
    :requires:
    :param actor: User instance of that user who makes the action.
    :param recipient: User instance, a list of User instances or string
                      'global' defining who should be notified.
    :param verb: Notification attribute with the right choice from the list.

    :optional:
    :param action_object: Model instance on which the verb was executed.
    :param key: String defining what kind of notification is going to be created.
    :param id_value: UUID value assigned to a specific element in the DOM.
    """
    key = kwargs.pop("key", "notification")
    id_value = kwargs.pop("id_value", None)
    if recipient == "global":
        users = get_user_model().objects.all().exclude(username=actor.username)
        for user in users:
            Notification.objects.create(
                actor=actor,
                recipient=user,
                verb=verb,
                action_object=kwargs.pop("action_object", None),
            )
        notification_broadcast(actor, key)

    elif isinstance(recipient, list):
        for user in recipient:
            Notification.objects.create(
                actor=actor,
                recipient=get_user_model().objects.get(username=user),
                verb=verb,
                action_object=kwargs.pop("action_object", None),
            )

    elif isinstance(recipient, get_user_model()):
        Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=kwargs.pop("action_object", None),
        )
        notification_broadcast(
            actor, key, id_value=id_value, recipient=recipient.username
        )

    else:
        pass


def delete_notification_handler(actor, recipient, verb, **kwargs):
    """
    Handler function to delete a Notification instance.
    :requires:
    :param actor: User instance of that user who makes the action.
    :param recipient: User instance, a list of User instances or string
                      'global' defining who should be notified.
    :param verb: Notification attribute with the right choice from the list.

    :optional:
    :param action_object: Model instance on which the verb was executed.
    :param key: String defining what kind of notification is going to be created.
    :param id_value: UUID value assigned to a specific element in the DOM.
    """
    key = kwargs.pop("key", "notification")
    id_value = kwargs.pop("id_value", None)
    if recipient == "global":
        users = get_user_model().objects.all().exclude(username=actor.username)
        for user in users:
            Notification.objects.filter(
                actor=actor,
                recipient=user,
                verb=verb,
                action_object_object_id=id_value,
            ).delete()
        notification_broadcast(actor, key)

    elif isinstance(recipient, list):
        for user in recipient:
            Notification.objects.filter(
                actor=actor,
                recipient=get_user_model().objects.get(username=user),
                verb=verb,
                action_object_object_id=id_value,
            ).delete()

    elif isinstance(recipient, get_user_model()):
        Notification.objects.filter(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object_object_id=id_value,
        ).delete()
        notification_broadcast(
            actor, key, id_value=id_value, recipient=recipient.username
        )

    else:
        pass


def notification_broadcast(actor, key, **kwargs):
    """Notification handler to broadcast calls to the recieve layer of the
    WebSocket consumer of this app.
    :requires:
    :param actor: User instance of that user who makes the action.
    :param key: String parameter to indicate the client which action to
                perform.

    :optional:
    :param id_value: UUID value assigned to a specific element in the DOM.
    :param recipient: String indicating the name of that who needs to be
                      notified.
    """
    channel_layer = get_channel_layer()
    id_value = kwargs.pop("id_value", None)
    recipient = kwargs.pop("recipient", None)
    payload = {
        "type": "receive",
        "key": key,
        "actor_name": actor.username,
        "id_value": id_value,
        "recipient": recipient,
    }
    async_to_sync(channel_layer.group_send)("notifications", payload)
