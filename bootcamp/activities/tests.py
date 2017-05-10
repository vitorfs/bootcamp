from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.activities.models import Activity


class TestModels(TestCase):
    """TestCase class to test the models functionality
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )

    def test_register_fav_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='F'
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(str(activity), 'F')
        self.assertNotEqual(str(activity), 'f')
