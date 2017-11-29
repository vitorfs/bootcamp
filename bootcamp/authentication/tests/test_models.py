from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from bootcamp.feeds.models import Feed
from bootcamp.authentication.models import Profile
from bootcamp.activities.models import Notification
from bootcamp.questions.models import Question, Answer


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
        self.another_user = get_user_model().objects.create_user(
            username='another_test_user',
            email='another_test@gmail.com',
            password='top_secret'
        )
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile_two = Profile.objects.get(
            user=self.other_user,
        )
        self.notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            notification_type='L',
            is_read=False
        )
        self.feed = Feed.objects.create(
            user=self.other_user,
            post='A not so long text',
            likes=0,
            comments=0
        )
        self.question = Question.objects.create(
            user=self.other_user, title='This is a sample question',
            description='This is a sample question description',
            tags='test1,test2')
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            description='A reaaaaally loooong content',
            votes=0,
            is_accepted=True
        )
        self.profile.url = 'trybootcamp.vitorfs.com'
        self.profile.location = 'My City'
        self.profile.job_title = 'Master of Defense Against the Dark Arts.'
        self.profile.save()

    def test_object_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.profile_two, Profile))
        self.assertTrue(isinstance(self.profile.user, User))

    def test_return_url(self):
        self.assertEqual(self.profile.get_url(),
                         'http://trybootcamp.vitorfs.com')

    def test_return_screen_name(self):
        self.assertEqual(self.profile.get_screen_name(), self.user.username)

    def test_return_str_(self):
        self.assertEqual(str(self.profile), 'test_user')

    def test_liked_notification(self):
        liked_count = Notification.objects.filter(
            notification_type='L').count()
        self.user.profile.notify_liked(self.feed)
        new_liked_count = Notification.objects.filter(
            notification_type='L').count()
        assert liked_count < new_liked_count

    def test_unliked_notification(self):
        self.user.profile.notify_liked(self.feed)
        liked_count = Notification.objects.filter(
            notification_type='L').count()
        self.user.profile.unotify_liked(self.feed)
        new_liked_count = Notification.objects.filter(
            notification_type='L').count()
        assert liked_count > new_liked_count

    def test_commented_notification(self):
        commented_count = Notification.objects.filter(
            notification_type='C').count()
        self.user.profile.notify_commented(self.feed)
        new_commented_count = Notification.objects.filter(
            notification_type='C').count()
        assert commented_count < new_commented_count

    def test_also_commented_notification(self):
        post = "A very thoughful comment."
        also_commented_count = Feed.get_comments(self.feed).count()
        self.feed.comment(user=self.another_user, post=post)
        self.user.profile.notify_also_commented(self.feed)
        new_also_commented_count = Feed.get_comments(self.feed).count()
        assert also_commented_count < new_also_commented_count

    def test_favorited_notification(self):
        favorited_count = Notification.objects.filter(
            notification_type='F').count()
        self.user.profile.notify_favorited(self.question)
        new_favorited_count = Notification.objects.filter(
            notification_type='F').count()
        assert favorited_count < new_favorited_count

    def test_unfavorited_notification(self):
        self.user.profile.notify_favorited(self.question)
        favorited_count = Notification.objects.filter(
            notification_type='F').count()
        self.user.profile.unotify_favorited(self.question)
        new_favorited_count = Notification.objects.filter(
            notification_type='F').count()
        assert favorited_count > new_favorited_count

    def test_answered_notification(self):
        answered_count = Notification.objects.filter(
            notification_type='A').count()
        self.user.profile.notify_answered(self.question)
        new_answered_count = Notification.objects.filter(
            notification_type='A').count()
        assert answered_count < new_answered_count
