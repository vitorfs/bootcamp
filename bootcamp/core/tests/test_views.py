from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.client = Client()
        self.other_client = Client()
        self.user = get_user_model().objects.create_user(
            username='test_user',
            email='test@gmail.com',
            password='top_secret'
        )
        self.other_user = get_user_model().objects.create_user(
            username='other_test_user',
            email='other_test@gmail.com',
            password='top_secret'
        )
        self.client.login(username='test_user', password='top_secret')

    def test_get_home_response(self):
        response = self.client.get(reverse('feeds'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('<Page 1 of 1>', str(response.context['feeds']))

    def test_get_home_response_no_logged(self):
        response = self.other_client.get(reverse('feeds'))
        self.assertRedirects(response, '/?next=/feeds/', status_code=302)

    def test_network_response(self):
        response = self.client.get(reverse('network'))
        self.assertEqual(response.status_code, 200)

    def test_network_response_no_logged(self):
        response = self.other_client.get(reverse('network'))
        self.assertRedirects(response, '/?next=/network/', status_code=302)

    def test_profile_respones(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bar_data' in response.context)

    def test_get_settings_response(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)

    def test_post_settings_response(self):
        response = self.client.post(reverse('settings'),
                                    {'first_name': 'first_name',
                                     'last_name': 'last_name',
                                     'job_title': 'job_title'})
        self.assertEqual(response.status_code, 200)

    def test_get_picture_response(self):
        response = self.client.get(reverse('picture'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('uploaded_picture' in response.context)
        self.assertEqual(response.context['uploaded_picture'], False)

    def test_post_picture_response(self):
        response = self.client.get(
            reverse('picture'), {'upload_picture': 'uploaded'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('uploaded_picture' in response.context)
        self.assertEqual(response.context['uploaded_picture'], True)
