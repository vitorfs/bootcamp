import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.news.models import News
from bootcamp.helpers import paginate_data


class NewsType(DjangoObjectType):
    """DjangoObjectType to acces the News model."""
    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        model = News

    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.liked_news.count()


class NewsPaginatedType(graphene.ObjectType):
    """A paginated type generic object to provide pagination to the news
    graph."""
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(NewsType)


class NewsQuery(object):
    all_news = graphene.List(NewsType)
    paginated_news = graphene.Field(NewsPaginatedType, page=graphene.Int())
    news = graphene.Field(NewsType, uuid_id=graphene.String())

    def resolve_all_news(self, info, **kwargs):
        return News.objects.filter(reply=False)

    def resolve_paginated_news(self, info, page):
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        qs = News.objects.filter(reply=False)
        return paginate_data(qs, page_size, page, NewsPaginatedType)

    def resolve_news(self, info, **kwargs):
        uuid_id = kwargs.get('uuid_id')

        if uuid_id is not None:
            return News.objects.get(uuid_id=uuid_id)

        return None
