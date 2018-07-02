from django.test import Client
from django.urls import reverse

from test_plus.test import TestCase

from bootcamp.notifications.models import Notification


class NewsViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.first_notification = Notification.objects.create(
                actor=self.user,
                recipient=self.other_user,
                verb="L"
            )
        self.second_notification = Notification.objects.create(
                actor=self.user,
                recipient=self.other_user,
                verb="C"
            )
        self.third_notification = Notification.objects.create(
                actor=self.other_user,
                recipient=self.user,
                verb="A"
            )
