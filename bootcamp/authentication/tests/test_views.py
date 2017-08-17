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
        self.other_client.login(username='other_test_user',
                                password='top_secret')

    def test_post_empty_response(self):
        response = self.client.post(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_post_signup(self):
        response = self.client.post(reverse('signup'),
                                    {'username': 'another_user',
                                     'email': 'email@amil.com',
                                     'password': 'random_pass',
                                     'confirm_password': 'random_pass'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_post_signup_redirects(self):
        response = self.client.post(reverse('signup'),
                                    {'username': 'another_user',
                                     'email': 'email@amil.com',
                                     'password': 'random_pass',
                                     'confirm_password': 'random_pass'},
                                    follow=True)
        self.assertRedirects(response, '/', status_code=302)

    def test_alternate_empty_response(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
