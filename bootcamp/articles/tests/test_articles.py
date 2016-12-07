from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory, TestCase

from bootcamp.articles.models import Article


class ArticleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_validate_article_edition(self):
        user2 = User.objects.create_user(username="teste12345",
                                         email="reallynice2@gmail.com",
                                         password="supersecret123")

        article = Article()
        article.title = "nicetitle"
        article.content = "nicecontent"
        article.create_user = user2
        article.create_user.id = user2.id
        article.save()
        self.client.login(username="teste1234", password="supersecret123")
        response = self.client.get(reverse('edit_article', kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('edit_article',
                                            kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="teste12345", password="supersecret123")
        response = self.client.get(reverse('edit_article', kwargs={'id': '1'}),
                                   user=user2)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('edit_article',
                                            kwargs={'id': '1'}))
        self.assertEqual(response.status_code, 200)
