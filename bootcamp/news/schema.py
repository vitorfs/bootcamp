import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.news.models import News


class NewsType(DjangoObjectType):
    """DjangoObjectType to acces the News model."""
    class Meta:
        model = News


class NewsQuery(object):
    all_news = graphene.List(NewsType)

    def resolve_all_news(self, info, **kwargs):
        return News.objects.all()
