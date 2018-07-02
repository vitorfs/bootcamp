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

    def test_return_values(self):
        assert isinstance(self.first_notification, Notification)
        assert isinstance(self.second_notification, Notification)
        assert isinstance(self.third_notification, Notification)
        assert str(self.first_notification) == "test_user liked 0 minutes ago"
        assert str(self.second_notification) == "test_user commented 0 minutes ago"
        assert str(self.third_notification) == "other_test_user answered 0 minutes ago"

    def test_return_unread(self):
        assert Notification.objects.unread().count() == 3
        assert self.first_notification in Notification.objects.unread()

    def test_mark_as_read_and_return(self):
        self.first_notification.mark_as_read()
        assert Notification.objects.read().count() == 1
        assert self.first_notification in Notification.objects.read()
        self.first_notification.mark_as_unread()
        assert Notification.objects.read().count() == 0

    def test_mark_all_as_read(self):
        Notification.objects.mark_all_as_read()
        assert Notification.objects.read().count() == 3
        Notification.objects.mark_all_as_unread(self.other_user)
        assert Notification.objects.read().count() == 1
        Notification.objects.mark_all_as_unread()
        assert Notification.objects.unread().count() == 3
        Notification.objects.mark_all_as_read(self.other_user)
        assert Notification.objects.read().count() == 2

    def test_get_most_recent(self):
        assert Notification.objects.get_most_recent().count() == 3

    def test_single_notification(self):
        Notification.objects.mark_all_as_read()
        obj = News.objects.create(
            user=self.user,
            content="This is a short content."
        )
        notification_handler(self.user, self.other_user, "C", action_object=obj)
        assert Notification.objects.unread().count() == 1

    def test_global_notification(self):
        Notification.objects.mark_all_as_read()
        notification_handler(self.user, "global", "C")
        assert Notification.objects.unread().count() == 1

    def test_list_notification(self):
        Notification.objects.mark_all_as_read()
        notification_handler(self.user, [self.user, self.other_user], "C")
        assert Notification.objects.unread().count() == 2
