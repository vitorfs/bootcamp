from django.contrib.auth import get_user_model
from django.test import TestCase

from bootcamp.feeds.models import Feed


class TestModels(TestCase):
    """TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.feed_one = Feed.objects.create(
            user=self.user,
            post='A one not so long text',
            likes=0,
            comments=0
        )
        self.feed_two = Feed.objects.create(
            user=self.user,
            post='A two not so long text',
            likes=0,
            comments=0
        )
        self.feed_three = Feed.objects.create(
            user=self.user,
            post='A three not so long text',
            likes=0,
            comments=0
        )
        self.sub_feed_one = Feed.objects.create(
            user=self.user,
            post='A not so long subtext one',
            likes=0,
            comments=0,
            parent=self.feed_one
        )
        self.sub_feed_two = Feed.objects.create(
            user=self.user,
            post='A not so long subtext two',
            likes=0,
            comments=0,
            parent=self.feed_one
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.feed_one, Feed))

    def test_feed_return_value(self):
        self.assertEqual(str(self.feed_one), 'A one not so long text')

    def test_get_feeds(self):
        assert self.feed_two in Feed.get_feeds(self.feed_three.id)
