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
        self.feed = Feed.objects.create(
            user=self.user,
            post='A not so long text',
            likes=0,
            comments=0
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.feed, Feed))

    def test_feed_return_value(self):
        self.assertEqual(str(self.feed), 'A not so long text')
