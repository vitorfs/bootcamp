from django.urls import reverse, resolve

from test_plus.test import TestCase


class TestUserURLs(TestCase):
    """Test URL patterns for users app."""

    def setUp(self):
        self.user = self.make_user()

    def test_list_reverse(self):
        """users:list should reverse to /."""
        self.assertEqual(reverse("users:list"), "/~users")

    def test_list_resolve(self):
        """/ should resolve to users:list."""
        self.assertEqual(resolve("/~users").view_name, "users:list")

    def test_redirect_reverse(self):
        """users:redirect should reverse to /~redirect/."""
        self.assertEqual(reverse("users:redirect"), "/~redirect/")

    def test_redirect_resolve(self):
        """/~redirect/ should resolve to users:redirect."""
        self.assertEqual(resolve("/~redirect/").view_name, "users:redirect")

    def test_detail_reverse(self):
        """users:detail should reverse to /testuser/."""
        self.assertEqual(
            reverse("users:detail", kwargs={"username": "testuser"}), "/testuser/"
        )

    def test_detail_resolve(self):
        """/testuser/ should resolve to users:detail."""
        self.assertEqual(resolve("/testuser/").view_name, "users:detail")

    def test_update_reverse(self):
        """users:update should reverse to /~update/."""
        self.assertEqual(reverse("users:update"), "/~update/")

    def test_update_resolve(self):
        """/~update/ should resolve to users:update."""
        self.assertEqual(resolve("/~update/").view_name, "users:update")

    def test_change_password_reverse(self):
        """users:account_change_password should reverse to /~password/."""
        self.assertEqual(reverse("users:account_change_password"), "/~password/")

    def test_change_password_resolve(self):
        """/~password/ should resolve to users:account_change_password."""
        self.assertEqual(resolve("/~password/").view_name, "users:account_change_password")
