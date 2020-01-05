from test_plus.test import TestCase


class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            "testuser",  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), "/users/testuser/")

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == "testuser"
        self.user.name = "Test User"
        assert self.user.get_profile_name() == "Test User"
