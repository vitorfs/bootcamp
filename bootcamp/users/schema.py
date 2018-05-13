import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.users.models import User


class UserType(DjangoObjectType):
    """DjangoObjectType to acces the User model."""
    class Meta:
        model = User


class UserQuery(object):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Users.objects.get(id=id)

        return None
