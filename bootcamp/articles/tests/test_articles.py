from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from bootcamp.articles.models import Article
from bootcamp.authentication.models import Profile
from django.contrib.auth.models import User

class ArticleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_validate_article_edition(self):
        c = Client()
        c.login(username="teste123", password="secret")

        user = User.objects.create_user(username="teste123",email="reallynice@gmail.com",
                password="supersecret123")

        article = Article()
        article.title = "nicetitle"
        article.content = "nicecontent"
        article.create_user = user
        article.save()

        response = self.client.get('/articles/edit/'+str(article.id), id=1 )
        self.assertEqual(response.status_code, 200)
        # request = self.factory.get('/articles/edit/1')
        # response = my_view(request)
        # self.assertEqual(request.status_code, 403)

        # response = self.client.get('/articles/edit/1')
        # self.assertEqual(response.status_code, 403)

    # def test_validate_article_creation(self):
    #     current

