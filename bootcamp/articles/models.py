from django.conf import settings
from django.db import models
from django.db.models import Count, F
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

from django_comments.signals import comment_was_posted
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit_selectize.managers import TaggableManager
from taggit.models import TaggedItemBase

from bootcamp.notifications.models import Notification, notification_handler


class ArticleQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    @staticmethod
    def get_counted_tags():
        return TaggedArticle.objects.filter(content_object__status='P').order_by('tag__id').\
            annotate(name=F('tag__name'), slug=F('tag__slug'),).values('slug', 'name').annotate(count=Count('tag'))


class TaggedArticle(TaggedItemBase):
    content_object = models.ForeignKey('Article', on_delete=models.CASCADE)


class Article(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="author",
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        _("Featured image"), upload_to="articles_pictures/%Y/%m/%d/"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = MarkdownxField()
    edited = models.BooleanField(default=False)
    tags = TaggableManager(through=TaggedArticle)
    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)


def notify_comment(**kwargs):  # pragma: no cover
    """Handler to be fired up upon comments signal to notify the author of a
    given article."""
    actor = kwargs["request"].user
    receiver = kwargs["comment"].content_object.user
    obj = kwargs["comment"].content_object
    notification_handler(actor, receiver, Notification.COMMENTED, action_object=obj)


comment_was_posted.connect(receiver=notify_comment)
