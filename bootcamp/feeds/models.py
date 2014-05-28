from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=2000)
    parent = models.ForeignKey('Feed', null=True, blank=True)

    class Meta:
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    def get_comments(self):
        return Feed.objects.filter(parent=self.pk)