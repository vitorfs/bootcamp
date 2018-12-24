import graphene
from graphene_django.types import DjangoObjectType

from bootcamp.users.models import User


class UserType(DjangoObjectType):
    """DjangoObjectType to acces the User model."""
    picture = graphene.String()
    name = graphene.String()

    class Meta:
        model = User

    def resolve_picture(self, *args, **kwargs):
        if self.picture:
            return self.picture.url

        return None

    def resolve_name(self, *args, **kwargs):
        if self.name:
            return self.name

        return self.username


class UserQuery(object):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return User.objects.get(id=id)

        return None
