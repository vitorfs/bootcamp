from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.activities.models import Activity, Notification
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

    def test_register_fav_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='F'
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(str(activity), 'F')
        self.assertNotEqual(str(activity), 'f')

    def test_register_like_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(str(activity), 'L')

    def test_register_like_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='L',
            is_read=False
        )
        test_string = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'.format(self.user.username, self.user.profile.get_screen_name(), self.feed.pk, notification.get_summary(self.feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'l')
