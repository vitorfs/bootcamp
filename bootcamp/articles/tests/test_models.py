from test_plus.test import TestCase

from bootcamp.articles.models import Article


class ArticlesModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.article = Article.objects.create(
            title="A really nice title",
            content="This is a really good content",
            status="P",
            user=self.user,
        )
        self.not_p_article = Article.objects.create(
            title="A really nice to-be title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            user=self.user,
        )

    def test_object_instance(self):
        assert isinstance(self.article, Article)
        assert isinstance(self.not_p_article, Article)
        assert isinstance(Article.objects.get_published()[0], Article)

    def test_return_values(self):
        assert self.article.status == "P"
        assert self.article.status != "p"
        assert self.not_p_article.status == "D"
        assert str(self.article) == "A really nice title"
        assert self.article in Article.objects.get_published()
        assert Article.objects.get_published()[0].title == "A really nice title"
        assert self.not_p_article in Article.objects.get_drafts()
