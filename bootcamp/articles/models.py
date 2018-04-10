from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

from slugify import slugify

from taggit.managers import TaggableManager


class Article(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name=_("Author"),
        on_delete=models.CASCADE)
    picture = models.ImageField(
        _('Main picture'), upload_to='article_pictures/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = models.TextField(max_length=5000)
    edited = models.BooleanField(default=False)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ("-create_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, to_lower=True, max_length=80)

        super(Article, self).save(*args, **kwargs)

    @staticmethod
    def get_published():
        articles = Article.objects.filter(status=Article.PUBLISHED)
        return articles

    @staticmethod
    def get_counted_tags():
        tag_dict = {}
        query = Article.objects.filter(status='P').annotate(tagged=Count(
            'tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()

    def get_summary(self):
        if len(self.content) > 255:
            return '{0}...'.format(self.content[:255])

        else:
            return self.content
