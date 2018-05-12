import graphene

from bootcamp.news.schema import NewsQuery


class Query(NewsQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)