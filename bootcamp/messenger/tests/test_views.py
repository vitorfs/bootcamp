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
            message="A short message",
            conversation=self.user,
            from_user=self.other_user,
        )
        self.message_three = Message.objects.create(
            user=self.other_user,
            message="A shorter message",
            conversation=self.other_user,
            from_user=self.user,
        )

    def test_user_messages(self):
        response = self.client.get(
            reverse('messages', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['message']),
                         "A not that long message")

    def test_delete_message_view(self):
        response = self.client.get(reverse('delete_message'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_inbox(self):
        response = self.client.get(reverse('inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['message']),
                         "A not that long message")

    def test_send_message_view(self):
        message_count = Message.objects.count()
        request = self.client.post(reverse('send_message'),
                                   {'to': 'other_test_user',
                                    'message': 'A not that short message'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(request.status_code, 200)
        new_msm_count = Message.objects.count()
        self.assertNotEqual(message_count, new_msm_count)

    def test_autoconversation(self):
        message_count = Message.objects.count()
        request = self.client.post(reverse('send_message'),
                                   {'to': 'test_user',
                                    'message': 'A not that short message'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(request.status_code, 200)
        new_msm_count = Message.objects.count()
        self.assertEqual(message_count, new_msm_count)

    def test_empty_conversation(self):
        message_count = Message.objects.count()
        request = self.client.post(reverse('send_message'),
                                   {'to': 'other_test_user',
                                    'message': ''},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(request.status_code, 200)
        new_msm_count = Message.objects.count()
        self.assertEqual(message_count, new_msm_count)
