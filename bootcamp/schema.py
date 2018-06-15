import graphene

from bootcamp.news.schema import NewsQuery
from bootcamp.users.schema import UserQuery


class Query(NewsQuery, UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
