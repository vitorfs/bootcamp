import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from bootcamp.notifications.models import Notification, notification_handler


class News(models.Model):
    """News model to contain small information snippets in the same manner as
    Twitter does."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name=_("Author"),
        on_delete=models.SET_NULL)
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=280)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name=_('Is a reply?'), default=False)
    objects = NewsManager()

    class Meta:
        name = "news"
        verbose_name = _("News")
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"uuid": self.uuid})

    def switch_like(self, user, news_obj):
        if user in self.liked.all():
            is_liked = False
            self.liked.remove(user)

        else:
            is_liked = True
            self.liked.add(user)
            notification_handler(user, self.user,
                Notification.LIKED, action_object=self)

        return is_liked

    def get_parent(self):
        the_parent = self.parent if self.parent else the_parent = self
        return the_parent

    def answer_to_news(self, target):
        pass

    def get_thread(self):
        pass

    def count_likers(self):
        return self.liked_set.count()

    def get_likers(self):
        return self.liked_set.all()
