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
        self.kwargs = {'content_type': 'application/json',
                       'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        self.client.login(username='test_user', password='top_secret')
        self.other_client.login(username='other_test_user', password='top_secret')
        self.title = 'A really nice to-be title'
        self.content = '''This is a really good content, just if somebody published
        it, that would be awesome, but no, nobody wants to publish it, because
        they know this is just a test, and you know than nobody wants to
        publish a test, just a test; everybody always wants the real deal.'''

    def test_index_articles(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        response_no_art = self.client.get(reverse(
            'article', kwargs={'slug': 'no-slug'}))
        self.assertEqual(response_no_art.status_code, 404)

    def test_individual_article(self):
        response = self.client.post(reverse('write'), {'title': self.title,
                                                       'content': self.content,
                                                       'tags': 'list, lists',
                                                       'status': 'P'})
        response_art = self.client.get(
            reverse('article', kwargs={'slug': 'a-really-nice-to-be-title'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_art.status_code, 200)
        self.assertEqual(response_art.context['article'].slug,
                         'a-really-nice-to-be-title')

    def test_drafts_workflow(self):
        response = self.client.post(reverse('write'), {'title': self.title,
                                                       'content': self.content,
                                                       'tags': 'list, lists',
                                                       'status': 'D'
                                                       })
        resp = self.client.get(reverse('drafts'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['drafts'][0].slug,
                        'a-really-nice-to-be-title')

    def test_filter_by_tag(self):
        response = self.client.post(reverse('write'), {'title': self.title,
                                                       'content': self.content,
                                                       'tags': 'list',
                                                       'status': 'P'})
        response_tag = self.client.get(
            reverse('tag', kwargs={'tag_name': 'list'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_tag.status_code, 200)
        self.assertTrue('list' in list(response_tag.context['popular_tags'])[0])

    def test_edit_article(self):
        response = self.client.post(reverse('write'), {'title': self.title,
                                                       'content': self.content,
                                                       'tags': 'list, lists',
                                                       'status': 'D'
                                                       })
        edit_response = self.client.get(
            reverse('edit_article', kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(edit_response.status_code, 200)
        # self.assertRedirects(edit_response, reverse('articles'))
        # self.assertRedirects(other_client_response, reverse('home'))
