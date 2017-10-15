from django.contrib.auth import get_user_model
from django.test import TestCase
from bootcamp.articles.models import Article, ArticleComment


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
        self.not_p_article = Article.objects.create(
            title='A really nice to-be title',
            content='''This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.''',
            create_user=self.user,
        )

    def test_object_instance(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertTrue(isinstance(self.article_comment, ArticleComment))
        self.assertTrue(isinstance(self.not_p_article, Article))
        self.assertTrue(isinstance(self.article.get_published()[0], Article))

    def test_return_values(self):
        self.assertEqual(self.article.status, 'P')
        self.assertNotEqual(self.article.status, 'p')
        self.assertEqual(self.not_p_article.status, 'D')
        self.assertEqual(str(self.article), 'A really nice title')
        self.assertEqual(self.article.get_content_as_markdown(),
                         '<p>This is a really good content</p>')
        self.assertTrue(self.article in self.article.get_published())
        self.assertEqual(self.article.get_published()[0].title,
                         'A really nice title')
        self.assertEqual(self.article.get_summary(), self.article.content)
        self.assertEqual(len(self.not_p_article.get_summary()), 258)
        self.assertEqual(self.article.get_summary_as_markdown(),
                         '<p>This is a really good content</p>')
        self.assertTrue(self.article_comment in self.article.get_comments())
        self.assertEqual(str(self.article_comment),
                         'test_user - A really nice title')
        self.assertEqual(self.article_comment.get_comment_as_markdown(),
                         '<p>A really nice comment</p>')
