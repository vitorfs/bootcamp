from django.test import TestCase
from bootcamp.feeds.models import Feed
from django.contrib.auth.models import User
from bootcamp.activities.models import Activity


class FeedsTest(TestCase):
    'HTTP code responses'
    PAGE_WAS_FOUND = 302
    CORRECT_RESPONSE = 200

    def setUp(self):
        'Setup users'
        User.objects.create(username="user1", password="password1")
        User.objects.create(username="user2", password="password2")
        User.objects.create(username="user3", password="password3")
        self.user1 = User.objects.get(username="user1")
        self.user2 = User.objects.get(username="user2")
        self.user3 = User.objects.get(username="user3")
        'Setup feeds'
        Feed.objects.create(post="My first post", user=self.user1)
        Feed.objects.create(post="Commenting feed1", user=self.user2)
        Feed.objects.create(post="Second comment in feed1", user=self.user1)
        self.feed1 = Feed.objects.get(post="My first post")
        self.feed2 = Feed.objects.get(post="Commenting feed1")
        self.feed3 = Feed.objects.get(post="Second comment in feed1")

    def tearDown(self):
        for user in User.objects.all():
            user.delete()
        for feed in Feed.objects.all():
            feed.delete()

    def test_get_feeds(self):
        assert self.feed1.post == unicode("My first post")

    def test_get_feeds_after(self):
        assert self.feed1.id < self.feed2.id
        assert self.feed1.id < self.feed3.id
        feeds = self.feed1.get_feeds_after(self.feed1.id) # returns a list with the posterior feeds
        posterior_feeds = []
        posterior_feeds.append(self.feed3)
        posterior_feeds.append(self.feed2)
        self.assertItemsEqual(feeds, posterior_feeds)

    def test_get_comments(self):
        feed_comment = self.feed1.comment(self.feed2.user, self.feed2.post)
        feed_test = Feed(user=self.user2, post="Commenting feed1", parent=self.feed1)
        self.assertTrue(feed_comment.parent == feed_test.parent)

    def test_calculate_comments(self):
        comment1 = self.feed1.comment(self.feed2.user, self.feed2.post)
        comment2 = self.feed1.comment(self.feed3.user, self.feed3.post)
        comments_quantity = 2
        self.assertEqual(self.feed1.calculate_comments(), comments_quantity)

    def test_calculate_likes(self):
        like = Activity.objects.create(activity_type=Activity.LIKE, feed=self.feed1.id, user=self.feed1.user)
        assert self.feed1.calculate_likes() == 1

    def test_get_likes(self):
        like = []
        like.append(Activity.objects.create(activity_type=Activity.LIKE, feed=self.feed1.id, user=self.feed1.user))
        self.assertItemsEqual(self.feed1.get_likes(), like)

    def test_get_likers(self):
        Activity.objects.create(activity_type=Activity.LIKE, feed=self.feed1.id, user=self.user2)
        Activity.objects.create(activity_type=Activity.LIKE, feed=self.feed1.id, user=self.user3)
        likers = []
        likers.append(self.user2)
        likers.append(self.user3)
        self.assertItemsEqual(self.feed1.get_likers(), likers)
