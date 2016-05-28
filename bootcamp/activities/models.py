from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape


class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (FAVORITE, 'Favorite'),
        (LIKE, 'Like'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
        )

    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    feed = models.IntegerField(null=True, blank=True)
    question = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        return self.activity_type

#    def save(self, *args, **kwargs):
#        super(Activity, self).save(*args, **kwargs)
#        if self.activity_type == Activity.FAVORITE:
#            Question = models.get_model('questions', 'Question')
#            question = Question.objects.get(pk=self.question)
#            user = question.user
#            user.profile.reputation = user.profile.reputation + 5
#            user.save()


class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    FAVORITED = 'F'
    ANSWERED = 'A'
    ACCEPTED_ANSWER = 'W'
    EDITED_ARTICLE = 'E'
    ALSO_COMMENTED = 'S'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (FAVORITED, 'Favorited'),
        (ANSWERED, 'Answered'),
        (ACCEPTED_ANSWER, 'Accepted Answer'),
        (EDITED_ARTICLE, 'Edited Article'),
        (ALSO_COMMENTED, 'Also Commented'),
        )

    _LIKED_TEMPLATE = u'<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'
    _COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'
    _FAVORITED_TEMPLATE = u'<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'
    _ANSWERED_TEMPLATE = u'<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'
    _ACCEPTED_ANSWER_TEMPLATE = u'<a href="/{0}/">{1}</a> accepted your answer: <a href="/questions/{2}/">{3}</a>'
    _EDITED_ARTICLE_TEMPLATE = u'<a href="/{0}/">{1}</a> edited your article: <a href="/article/{2}/">{3}</a>'
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    feed = models.ForeignKey('feeds.Feed', null=True, blank=True)
    question = models.ForeignKey('questions.Question', null=True, blank=True)
    answer = models.ForeignKey('questions.Answer', null=True, blank=True)
    article = models.ForeignKey('articles.Article', null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __unicode__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        elif self.notification_type == self.FAVORITED:
            return self._FAVORITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.ANSWERED:
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.question.pk,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == self.ACCEPTED_ANSWER:
            return self._ACCEPTED_ANSWER_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.answer.question.pk,
                escape(self.get_summary(self.answer.description))
                )
        elif self.notification_type == self.EDITED_ARTICLE:
            return self._EDITED_ARTICLE_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.article.slug,
                escape(self.get_summary(self.article.title))
                )
        elif self.notification_type == self.ALSO_COMMENTED:
            return self._ALSO_COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.profile.get_screen_name()),
                self.feed.pk,
                escape(self.get_summary(self.feed.post))
                )
        else:
            return 'Ooops! Something went wrong.'

    def get_summary(self, value):
        summary_size = 50
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])

        else:
            return value
