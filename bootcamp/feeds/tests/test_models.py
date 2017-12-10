from django.test import TestCase

from bootcamp.factories import UserFactory, FeedsFactory
from bootcamp.feeds.models import Feed
from bootcamp.activities.models import Activity


class TestModels(TestCase):
    """TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.feed_one = FeedsFactory(
            user=self.user,
            post='A one not so long text'
        )
        self.feed_two = FeedsFactory(user=self.user)
        self.feed_three = FeedsFactory(user=self.user)
        self.sub_feed_one = FeedsFactory(
            user=self.user,
            parent=self.feed_one
        )
        self.sub_feed_two = FeedsFactory(
            user=self.user,
            parent=self.feed_one
        )

    def test_instance_values(self):
        self.assertTrue(isinstance(self.feed_one, Feed))

    def test_feed_return_value(self):
        self.assertEqual(str(self.feed_one), 'A one not so long text')

    def test_get_feeds(self):
        assert self.feed_two in Feed.get_feeds(self.feed_three.id)

    def test_get_feeds_after(self):
        assert self.feed_two in Feed.get_feeds_after(self.feed_one.id)

    def test_get_comments(self):
        assert self.sub_feed_one in self.feed_one.get_comments()
        assert self.sub_feed_two in self.feed_one.get_comments()

    def test_calculate_likes(self):
        old_likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                            feed=self.feed_one.pk).count()
        old_attrib_likes = self.feed_one.calculate_likes()
        activity = Activity.objects.create(
            user=self.user,
            activity_type='L',
            feed=self.feed_one.pk
        )
        new_likes = Activity.objects.filter(activity_type=Activity.LIKE,
                                            feed=self.feed_one.pk).count()
        new_attrib_likes = self.feed_one.calculate_likes()
        assert old_likes < new_likes
        assert isinstance(activity, Activity)
        assert old_attrib_likes < new_attrib_likes

    def test_get_likers(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='L',
            feed=self.feed_one.pk
        )
        likers = self.feed_one.get_likers()
        assert isinstance(activity, Activity)
        assert self.user in likers

    def test_calculate_comments(self):
        assert self.feed_one.comments == 0
        assert self.feed_one.calculate_comments() == 2
        assert self.feed_one.comments == 2
