from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from bootcamp.factories import UserFactory, FeedsFactory


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = UserFactory()
        self.client = Client()
        self.client.login(username='test_user', password='top_secret')
        # self.client.login(
        #     username=self.other_user.username,
        #     password=self.other_user.password
        # )
        self.feed = FeedsFactory(
            user=self.user
        )

    def test_feeds_view(self):
        request = self.client.get(reverse('feeds'))
        assert request.status_code == 200

    def test_feed_alone(self):
        request = self.client.get(reverse('feed', args=[self.feed.id]))
        assert request.status_code == 200

    def test_load_view(self):
        request = self.client.get(reverse('load'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert request.status_code == 200
