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
        self.kwargs = {'content_type': 'application/json',
                       'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.client.login(username='test_user', password='top_secret')

    def test_index_articles(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        response_no_art = self.client.get(reverse(
            'article', kwargs={'slug': 'no-slug'}))
        self.assertEqual(response_no_art.status_code, 404)

    def test_individual_article(self):
        title = 'A really nice to-be title'
        content = '''This is a really good content, just if somebody published
        it, that would be awesome, but no, nobody wants to publish it, because
        they know this is just a test, and you know than nobody wants to
        publish a test, just a test; everybody always wants the real deal.'''
        response = self.client.post(reverse('write'), {'title': title,
                                                       'content': content,
                                                       'status': 'P'})
        response_arts = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_arts.context['article'].slug,
                         'a-really-nice-to-be-title')
