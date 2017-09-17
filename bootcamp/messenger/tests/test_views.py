from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from bootcamp.messenger.models import Message


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.client = Client()
        self.other_client = Client()
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
        self.client.login(username='test_user', password='top_secret')
        self.other_client.login(
            username='other_test_user', password='top_secret')
        self.message_one = Message.objects.create(
            user=self.user,
            message="A not that long message",
            conversation=self.user,
            from_user=self.other_user,
        )
        self.message_two = Message.objects.create(
            user=self.user,
            message="A not that long message",
            conversation=self.user,
            from_user=self.other_user,
        )
        self.message_three = Message.objects.create(
            user=self.other_user,
            message="A shorter message",
            conversation=self.other_user,
            from_user=self.user,
        )
