from django.db import models
from django.contrib.auth.models import User
from bootcamp.activities.models import Activity

class Feed(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=2000)
    parent = models.ForeignKey('Feed', null=True, blank=True)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Feed'
        verbose_name_plural = 'Feeds'
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    def get_comments(self):
        return Feed.objects.filter(parent=self.pk)

    def calculate_likes(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def get_likers(self):
        likes = Activity.objects.filter(activity_type=Activity.LIKE, feed=self.pk)
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers