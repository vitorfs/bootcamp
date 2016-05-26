from django.test import TestCase
from bootcamp.messenger.models import Message
from django.contrib.auth.models import User


class MessageTest(TestCase):

    def setUp(self):
        User.objects.create(username="user1", password="password1")
        User.objects.create(username="user2", password="password2")
        self.sender_user = User.objects.get(username="user1")
        self.reciever_user = User.objects.get(username="user2")
        self.congratulations = "Hello. How are you?"
        Message.objects.create(
            from_user=self.sender_user,
            message=self.congratulations,
            user=self.sender_user,
            conversation=self.reciever_user,
            is_read=True)
        self.message_sent = Message.objects.get(message=self.congratulations)

    def test_send_message(self):
        self.assertTrue(self.congratulations, self.message_sent.message)

    def test_verify_message_size(self):
        pass
