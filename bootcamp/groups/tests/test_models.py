from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group


class TestGroupsModels(TestCase):
    """
    TestCase class to test the groups models.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.group = Group.objects.create(
            title='test title 1',
            description='some random words'
        )
        # Make `user` the admin & subscriber.
        self.group.admins.add(self.user)
        self.group.subscribers.add(self.user)

        self.other_group = Group.objects.create(
            title='test title 2',
            description='some random words'
        )

    def test_instance_values(self):
        """Test group instance values."""
        self.assertTrue(isinstance(self.group, Group))

    def test_group_return_value(self):
        """Test group string return value."""
        self.assertEqual(str(self.group), 'test title 1')

    def test_groups_list_count(self):
        """Test to count groups."""
        self.assertEqual(Group.objects.count(), 2)

    def test_get_admins_method(self):
        """Test get admins method."""
        self.assertEqual(len(self.group.get_admins()), 1)
