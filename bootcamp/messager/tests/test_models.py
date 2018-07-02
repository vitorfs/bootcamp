from test_plus.test import TestCase

from bootcamp.messager.models import Message


class MessagerModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.first_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="A not that long message."
        )
        self.second_message = Message.objects.create(
            sender=self.user,
            recipient=self.other_user,
            message="A follow up message."
        )
        self.third_message = Message.objects.create(
            sender=self.other_user,
            recipient=self.user,
            message="An answer message."
        )

    def test_object_instance(self):
        assert isinstance(self.first_message, Message)

    def test_return_values(self):
        assert str(self.first_message) == "A not that long message."
        assert self.first_message.message == "A not that long message."

    def test_conversation(self):
        conversation = Message.objects.get_conversation(
            self.user, self.other_user)
        assert conversation.last().message == "An answer message."

    def test_recent_conversation(self):
        active_user = Message.objects.get_most_recent_conversation(
            self.user)
        assert active_user == self.other_user

    def test_single_marking_as_read(self):
        self.first_message.mark_as_read()
        read_message = Message.objects.filter(unread=False)
        assert read_message[0] == self.first_message

    def test_sending_new_message(self):
        initial_count = Message.objects.count()
        Message.send_message(
            self.other_user, self.user, "A follow up answer message."
        )
        assert Message.objects.count() == initial_count + 1
