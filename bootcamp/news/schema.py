import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.news.models import News


class NewsType(DjangoObjectType):
    """DjangoObjectType to acces the News model."""
    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        model = News

    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.liked.count()


class NewsQuery(object):
    all_news = graphene.List(NewsType)
    news = graphene.Field(NewsType, uuid_id=graphene.String())

    def resolve_all_news(self, info, **kwargs):
        return News.objects.filter(reply=False)

    def resolve_news(self, info, **kwargs):
        uuid_id = kwargs.get('uuid_id')

        if uuid_id is not None:
            return News.objects.get(uuid_id=uuid_id)

        return None
