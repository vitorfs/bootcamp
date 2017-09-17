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

    def test_object_instance(self):
        self.assertTrue(isinstance(self.message_one, Message))

    def test_return_values(self):
        self.assertEqual(str(self.message_one), "A not that long message")
        self.assertEqual(self.message_one.message, "A not that long message")
        self.assertEqual(self.message_three.message, "A shorter message")
        self.assertEqual(Message.get_conversations(self.user)[0]['last'],
                         self.message_two.date)
        self.assertEqual(Message.get_conversations(self.other_user)[0]['last'],
                         self.message_three.date)

    def test_sending_new_message(self):
        new_message = Message.send_message(
            self.other_user, self.user, "A short message")
        self.assertTrue(isinstance(new_message, Message))
        self.assertEqual(Message.get_conversations(self.other_user)[0]['last'],
                         new_message.date)
        self.assertEqual(new_message.message, "A short message")
