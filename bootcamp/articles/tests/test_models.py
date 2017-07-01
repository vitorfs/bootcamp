from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.articles.models import Article, ArticleComment, Tag


class TestModels(TestCase):
    """TestCase class to test the models functionality
    """

    def setUp(self):
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
        self.article = Article.objects.create(
            title='A really nice title',
            content='This is a really good content',
            status='P',
            create_user=self.user,
        )
        self.article_comment = ArticleComment.objects.create(
            article=self.article,
            comment='A really nice comment',
            user=self.user,
        )
