import factory

from django.contrib.auth import get_user_model

from bootcamp.feeds.models import Feed
from bootcamp.activities.models import Activity


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    email = factory.LazyAttribute(
        lambda obj: '{}@example.com'.format(obj.username))
    password = 'password'


class FeedsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feed

    user = factory.SubFactory(UserFactory)
    post = 'A really well though not so random text.'


class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    user = factory.SubFactory(UserFactory)
    feed = factory.SubFactory(FeedsFactory)
