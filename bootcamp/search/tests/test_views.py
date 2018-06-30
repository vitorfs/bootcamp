from django.urls import reverse
from django.test import Client

from test_plus.test import TestCase

from bootcamp.articles.models import Article
from bootcamp.qa.models import Question
from bootcamp.news.models import News


class SearchViewsTests(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.title = "A really nice to-be first title "
        self.content = """This is a really good content, just if somebody
        published it, that would be awesome, but no, nobody wants to publish
        it, because they know this is just a test, and you know than nobody
        wants to publish a test, just a test; everybody always wants the real
        deal."""
        self.article = Article.objects.create(
            user=self.user, title="A really nice first title",
            content=self.content, tags="list, lists", status="P")
        self.article_2 = Article.objects.create(user=self.other_user,
                                                title="A first bad title",
                                                content="First bad content",
                                                tags="bad", status="P")
        self.question_one = Question.objects.create(
            user=self.user, title="This is the first sample question",
            content="This is a sample question description for the first time",
            tags="test1,test2")
        self.question_two = Question.objects.create(
            user=self.user,
            title="The first shortes title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it first, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            has_answer=True, tags="test1,test2"
        )
        self.news_one = News.objects.create(user=self.user,
                                            content="This is the first lazy content.")

    def test_news_search_results(self):
        response = self.client.get(
            reverse("search:results"), {'query': 'This is'})
        assert response.status_code == 200
        assert self.news_one in response.context["news_list"]
        assert self.question_one in response.context["questions_list"]
        assert self.question_two in response.context["questions_list"]
        assert self.article in response.context["articles_list"]

    def test_questions_suggestions_results(self):
        response = self.client.get(
            reverse("search:suggestions"), {'term': 'first'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.json()[0]['value'] == "first_user"
        assert response.json()[1]['value'] == "A first bad title"
        assert response.json()[2]['value'] == "A really nice first title"
        assert response.json()[3]['value'] == "The first shortes title"
        assert response.json()[4]['value'] == "This is the first sample question"
