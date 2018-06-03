import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from taggit.managers import TaggableManager


class QuestionQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_answered(self):
        """Returns only items which has been marked as answered in the current
        queryset"""
        return self.filter(has_answer=True)

    def get_unanswered(self):
        """Returns only items which has not been marked as answered in the
        current queryset"""
        return self.filter(has_answer=False)

    def get_counted_tags(self):
        """Returns a dict element with tags and its count to show on the UI."""
        tag_dict = {}
        query = self.all().annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Question(models.Model):
    """Model class to contain every question in the forum."""
    OPEN = "O"
    CLOSED = "C"
    DRAFT = "D"
    STATUS = (
        (OPEN, _("Open")),
        (CLOSED, _("Closed")),
        (DRAFT, _("Draft")),
    )
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = models.TextField(max_length=2500)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name="liked")
    has_answer = models.BooleanField(default=False)
    total_votes = models.IntegerField(default=0)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)
    objects = QuestionQuerySet.as_manager()


    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.uuid_id}",
                                to_lower=True, max_length=80)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

    def get_answers(self):
        return Answer.objects.filter(question=self)

    def count_answers(self):
        return Answer.objects.filter(question=self).count()

    def get_likers(self):
        return self.liked.all()

    def count_likers(self):
        return self.liked.count()

    def get_accepted_answer(self):
        return Answer.objects.get(question=self, is_answer=True)


class Answer(models.Model):
    """Model class to contain every answer in the forum and to link it
    to its respective question."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=2500)
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_answer = models.BooleanField(default=False)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
        blank=True, related_name="liked")
    total_votes = models.IntegerField(default=0)
    up_votes = models.PositiveIntegerField(default=0)
    down_votes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-is_answer", "-timestamp"]
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.uuid_id}",
                                to_lower=True, max_length=80)

        super().save(*args, **kwargs)

    def __str__(self):  # pragma: no cover
        return self.content

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

    def accept_answer(self):
        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)
        self.is_answer = True
        self.save()
        self.question.has_answer = True
        self.question.save()

    def get_likers(self):
        return self.liked.all()

    def count_likers(self):
        return self.liked.count()


class Vote(models.Model):
    """Model class to host every vote, made with ContentType framework to
    allow a single model connected to Questions and Answers."""
    uuid_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    vote_content_type = models.ForeignKey(ContentType,
        blank=True, null=True, related_name="notify_vote",
        on_delete=models.CASCADE)
    vote_object_id = models.CharField(
        max_length=50, blank=True, null=True)
    vote = GenericForeignKey(
        "vote_content_type", "vote_object_id")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")

    @staticmethod
    def vote_on(instance, value):
        Vote.objects.create(
            user=instance.user,
            value=value,
            vote=instance
        )
        votes = Vote.objects.filter(vote=instance)
        instance.up_votes = votes.objects.filter(value=True).count()
        instance.down_votes = votes.objects.filter(value=False).count()
        instance.total_votes = instance.up_votes - instance.down_votes
        instance.save()
