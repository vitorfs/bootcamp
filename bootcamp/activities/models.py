import json

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.utils.translation import ugettext_lazy as _


class Activity(models.Model):
    LIKE = 'L'
    COMMENT = 'C'
    ANSWER = 'A'
    VOTE = 'U'
    RESHARE = 'S'
    NOTIFICATION_TYPES = (
        (LIKE, _('Liked')),
        (COMMENT, _('Commented')),
        (ANSWER, _('Answered')),
        (VOTE, _('Voted on')),
        (RESHARE, _('Reshared')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=1, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __str__(self):
        return self.activity_type

    @staticmethod
    def daily_activity(user):
        """Static method to retrieve daily statistical information about the
        user activity.
        @requires:  user - Instance from the User Django model.
        @returns:   Two JSON arrays, the first one is dates which contains all
                    the dates with activity records, and the second one is
                    datapoints containing the sum of all the activity than had
                    place in every single day.

        Both arrays keep the same order, so there is no need to order them.
        """
        query = Activity.objects.filter(user=user).annotate(day=TruncDay(
            'timestamp')).values('day').annotate(c=Count('id')).values('day', 'c')
        try:
            dates, datapoints = zip(*[[a['c'], str(a['day'].date())] for a in query])
            return json.dumps(dates), json.dumps(datapoints)

        except ValueError:
            return json.dumps(0), json.dumps(0)
