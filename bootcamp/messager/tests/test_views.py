from django.test import Client
from django.urls import reverse

from test_plus.test import TestCase

from bootcamp.messager.models import Message


class MessagerViewsTests(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
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

    def test_user_messages(self):
        response = self.client.get(reverse("messager:messages_list"))
        assert response.status_code == 200
        assert str(response.context["message"]) == "A not that long message."

    def test_user_conversation(self):
        response = self.client.get(
            reverse("messager:conversation_detail",
                    kwargs={"username": self.user.username}))
        assert response.status_code == 200
        assert str(response.context["active"]) == "first_user"

    def test_send_message_view(self):
        message_count = Message.objects.count()
        request = self.client.post(reverse("messager:send_message"),
                                   {"to": "second_user",
                                    "message": "A new short message"},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert request.status_code == 200
        new_msm_count = Message.objects.count()
        assert new_msm_count == message_count + 1

    def test_wrong_requests_send_message(self):
        get_request = self.client.get(reverse("messager:send_message"),
                                   {"to": "second_user",
                                    "message": "A new short message"},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        no_ajax_request = self.client.get(reverse("messager:send_message"),
                                   {"to": "second_user",
                                    "message": "A new short message"})
        same_user_request = self.client.post(reverse("messager:send_message"),
                                   {"to": "first_user",
                                    "message": "A new short message"},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        no_lenght_request = self.client.post(reverse("messager:send_message"),
                                   {"to": "second_user",
                                    "message": ""},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert get_request.status_code == 405
        assert no_ajax_request.status_code == 400
        assert same_user_request.status_code == 200
        assert no_lenght_request.status_code == 200

    def test_message_reception_view(self):
        request = self.client.get(reverse("messager:receive_message"),
                                   {"message_id": self.third_message.uuid_id},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert b"An answer message." in request.content

    def test_wrong_request_recieve_message_view(self):
        request = self.client.post(reverse("messager:receive_message"),
                                   {"message_id": self.third_message.uuid_id},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert request.status_code == 405
