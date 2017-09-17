from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.messenger.models import Message


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
        self.message_one = Message.objects.create(
            user=self.user,
            message="A not that long message",
            conversation=self.user,
            from_user=self.other_user,
        )

    def test_object_instance(self):
        self.assertTrue(isinstance(self.message, Message))
