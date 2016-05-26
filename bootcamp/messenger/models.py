from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Max

class Message(models.Model):
    user = models.ForeignKey(User, related_name='+')
    message = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(User, related_name='+')
    from_user = models.ForeignKey(User, related_name='+')
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ('date',)
        db_table = 'messages_message'

    def __unicode__(self):
        return self.message

    @staticmethod
    def send_message(from_user, to_user, message):
        message = message[:1000]
        current_user_message = Message(
            from_user=from_user,
            message=message,
            user=from_user,
            conversation=to_user,
            is_read=True)
        current_user_message.save()
        Message(from_user=from_user,
                conversation=from_user,
                message=message,
                user=to_user).save()
        return current_user_message

    @staticmethod
    def get_conversations(user):
        conversations = Message.objects.filter(
            user=user).values('conversation').annotate(
            last=Max('date')).order_by('-last')
        users = []
        for conversation in conversations:
            users.append({
                'user': User.objects.get(pk=conversation['conversation']),
                'last': conversation['last'],
                'unread': Message.objects.filter(
                    user=user,
                    conversation__pk=conversation['conversation'],
                    is_read=False).count(),
                })
        return users

    #Message.objects.filter(is_read=False, user__username='vitorfs').values('to_user').annotate(Count('to_user')).order_by()
    #Message.objects.filter(user__username='vitorfs').values('to_user', 'last').annotate(last=Max('date')).order_by()
    #Message.objects.filter(user__username='vitorfs').values('to_user').annotate(last=Max('date')).order_by('last')
