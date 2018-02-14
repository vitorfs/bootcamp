from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from bootcamp.factories import UserFactory, FeedsFactory
from bootcamp.feeds.models import Feed


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
        self.feeds = FeedsFactory.create_batch(30)

    def test_feeds_view(self):
        request = self.client.get(reverse('feeds'))
        assert request.status_code == 200

    def test_feed_alone(self):
        request = self.client.get(reverse('feed', args=[self.feed.id]))
        assert request.status_code == 200

    def test_load_view(self):
        request = self.client.get(reverse('load'),
                                  {'from_feed': 1,
                                   'page': 2,
                                   'feed_source': 'all'},
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert request.status_code == 200

    def test_load_diff_source_view(self):
        request = self.client.get(reverse('load'),
                                  {'from_feed': 1,
                                   'page': 2,
                                   'feed_source': '1'},
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert request.status_code == 200

    def test_load_new_feed(self):
        request = self.client.get(reverse('load_new'), {'last_feed': '1'},
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert request.status_code == 200

    def test_check_feeds(self):
        request = self.client.get(reverse('check'),
                                  {'last_feed': '10', 'feed_source': 'all'},
                                  HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert request.status_code == 200
        assert int(request.content) > 1

    def test_post_feed_view(self):
        post = 'A not that long string because I still do not need to go there'
        feeds_count = Feed.objects.all().count()
        request = self.client.post(reverse('post'),
                                   {'last_feed': '1', 'post': post},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        feeds_new_count = Feed.objects.all().count()
        feed = Feed.objects.first()
        assert request.status_code == 200
        assert feeds_count < feeds_new_count
        assert feed.post == post
