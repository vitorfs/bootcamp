from test_plus.test import TestCase

from bootcamp.news.models import News
from bootcamp.notifications.models import Notification, notification_handler


class NotificationsModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
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
