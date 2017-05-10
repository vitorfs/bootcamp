from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.activities.models import Activity, Notification
from bootcamp.feeds.models import Feed
from bootcamp.questions.models import Question


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
        self.question = Question.objects.create(
            user=self.user,
            title='A Short Title',
            description='A reaaaaally loooong content',
            favorites=0,
            has_accepted_answer=True
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

    def test_register_comm_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='C',
            is_read=False
        )
        test_string = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'.format(self.user.username, self.user.profile.get_screen_name(), self.feed.pk, notification.get_summary(self.feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'c')

    def test_register_fav_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            question=self.question,
            notification_type='F',
            is_read=False
        )
        test_string = '<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'.format(self.user.username, self.user.profile.get_screen_name(), self.question.pk, notification.get_summary(self.question.title))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'f')
