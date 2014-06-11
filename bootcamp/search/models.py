from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Message(models.Model):
    conversation_id = models.IntegerField()
    inbox_user = models.ForeignKey(User, related_name='+')
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(max_length=4000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_reply = models.DateTimeField(blank=True, null=True)
    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    parent = models.ForeignKey('Message', null=True, blank=True, related_name='+')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('-date',)

    def __unicode__(self):
        return self.subject

    def get_replys(self):
        return Message.objects.filter(parent=self).order_by('date')