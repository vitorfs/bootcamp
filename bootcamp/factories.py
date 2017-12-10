from django.contrib.auth import get_user_model

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'username_{}'.format(n))
    email = factory.LazyAttribute(
        lambda obj: '{}@example.com'.format(obj.username))
    password = 'password'
