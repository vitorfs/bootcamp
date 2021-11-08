from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client, TestCase

from ..models import Group


class TestGroupsViews(TestCase):
    """
    TestCase class to test the groups views.
    """

    def setUp(self):
        # This client will be logged in, admin & subscriber of the `group`.
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.client.login(username='test_user', password='top_secret')
        # Another logged in client.
        self.other_client = Client()
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.other_client.login(
            username='other_test_user', password='top_secret')
        # Anonymous client.
        self.anonymous_client = Client()
        # This user will be banned in the `group`.
        self.user_to_ban = get_user_model().objects.create_user(
            username='user_to_ban',
            email='user_to_ban@gmail.com',
            password='top_secret'
        )
        self.group = Group.objects.create(
            title='test title 1',
            description='some random words'
        )
        # Make `user` the admin & subscriber.
        self.group.admins.add(self.user)
        self.group.subscribers.add(self.user)
        # Ban `other_user` from group.
        self.group.banned_users.add(self.other_user)
        self.other_group = Group.objects.create(
            title='test title 2',
            description='some random words'
        )

    # def test_groups_page_view(self):
    #     """Test groups list view."""
    #     response = self.client.get(reverse('view_all_groups'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('groups' in response.context.keys())
    #     self.assertTrue('test title 1' in str(response.context['groups']))
    #
    # def test_banned_users_list(self):
    #     """Test banned users list view."""
    #     url = reverse('banned_users', kwargs={'group': self.group.slug})
    #     # When admin requests the list.
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('users' in response.context.keys())
    #     self.assertEqual(len(response.context['users']), 1)
    #     # When anonymous user requests the list.
    #     other_response = self.anonymous_client.get(url)
    #     self.assertRedirects(other_response, other_response.url, status_code=302)
    #
    # def test_ban_user_view(self):
    #     """Test ban user view functionality."""
    #     response = self.client.get(
    #         reverse('ban_user', kwargs={'group': self.group.slug,
    #                                     'user_id': self.user_to_ban.id}))
    #     self.assertRedirects(response,
    #                          reverse('banned_users', kwargs={'group': self.group.slug}), status_code=302)
    #
    # def test_user_subscription_list_view(self):
    #     """Test the users subscriptions list."""
    #     response = self.client.get(
    #         reverse('user_subscription_list', kwargs={'username': self.user.username}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('subscriptions' in response.context.keys())
    #     self.assertEqual(len(response.context['subscriptions']), 1)
    #     self.assertTrue('test title 1' in str(response.context['subscriptions']))
    #
    # def test_user_created_groups_page_view(self):
    #     """Test groups list created by certain user."""
    #     response = self.client.get(
    #         reverse('user_created_groups', kwargs={'username': self.user.username}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('user_groups' in response.context.keys())
    #     self.assertEqual(len(response.context['user_groups']), 1)
    #     self.assertTrue('test title 1' in str(response.context['user_groups']))
    #
    # def test_group_page_view(self):
    #     """Test group page view."""
    #     # logged in client
    #     response = self.client.get(
    #         reverse('group', kwargs={'group': self.group.slug}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('news' in response.context.keys())
    #     self.assertEqual(len(response.context['news']), 0)
    #     # anonymous client
    #     other_response = self.anonymous_client.get(
    #         reverse('group', kwargs={'group': self.group.slug}))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_create_group_view(self):
    #     """Test the creation of groups."""
    #     # Interent connection is required to make this test pass.
    #     current_groups_count = Group.objects.count()
    #     response = self.client.post(reverse('new_group'),
    #                                 {'title': 'Not much of a title',
    #                                  'description': 'babla', })
    #     self.assertEqual(response.status_code, 302)
    #     new_group = Group.objects.get(title='Not much of a title')
    #     self.assertEqual(new_group.title, 'Not much of a title')
    #     self.assertEqual(Group.objects.count(),
    #                      current_groups_count + 1)
    #
    # def test_subscribe_group(self):
    #     """Test the subscribed ajax call & response."""
    #     response = self.other_client.get(reverse('subscribe', kwargs={'group': self.group.slug}),
    #                                      HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    #     # `other_user` is banned in previous test so it'll raise PermissionDenied.
    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(self.group.subscribers.count(), 1)
    #
    # def test_edit_group_cover_view(self):
    #     """Test if non admin can edit group cover."""
    #     response = self.other_client.get(reverse('edit_group_cover', kwargs={'group': self.group.slug}))
    #     self.assertEqual(response.status_code, 403)
    #
    # def test_group_view_success_status_code(self):
    #     """Test group detail view with right url."""
    #     response = self.client.get(reverse('group', kwargs={'group': self.group.slug}))
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_group_view_not_found_status_code(self):
    #     """Test group detail view with wrong url."""
    #     response = self.client.get(reverse('group', kwargs={'group': 'does-not-exists'}))
    #     self.assertEqual(response.status_code, 404)
