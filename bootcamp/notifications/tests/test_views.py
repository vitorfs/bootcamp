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

    def test_notification_list(self):
        response = self.client.get(reverse("notifications:unread"))
        assert response.status_code == 200
        assert self.third_notification in response.context["notification_list"]

    def test_mark_all_as_read(self):
        response = self.client.get(reverse("notifications:mark_all_read"), follow=True)
        assert '/notifications/' in str(response.context["request"])
        assert Notification.objects.unread().count() == 2

    def test_mark_as_read(self):
        response = self.client.get(
            reverse("notifications:mark_as_read", kwargs={"slug": self.first_notification.slug}))
        assert response.status_code == 302
        assert Notification.objects.unread().count() == 2

    def test_latest_notifications(self):
        response = self.client.get(reverse("notifications:latest_notifications"))
        assert response.status_code == 200
        assert self.third_notification in response.context["notifications"]
