import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MessageQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_conversation(self, sender, recipient):
        """Returns all the messages sent between two users."""
        qs_one = self.filter(sender=sender, recipient=recipient)
        qs_two = self.filter(sender=recipient, recipient=sender)
        return qs_one.union(qs_two).order_by('-timestamp')


class Message(models.Model):
    """A private message sent between users.
    """
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='sent_messages',
        verbose_name=_("Sender"), null=True, on_delete=models.SET_NULL)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='received_messages', null=True,
        blank=True, verbose_name=_("Recipient"), on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(max_length=1000, blank=True)
    is_read = models.BooleanField(default=False)
    objects = MessageQuerySet.as_manager()

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.message
