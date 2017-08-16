from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase

from bootcamp.authentication.models import Profile


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
        self.profile = Profile.objects.get(
            user=self.user,
        )
        self.profile_two = Profile.objects.get(
            user=self.other_user,
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
