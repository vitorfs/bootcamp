from test_plus.test import TestCase

from bootcamp.news.models import News


class NewsModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.first_news = News.objects.create(
            user=self.user,
            content="This is a short content."
        )
        self.second_news = News.objects.create(
            user=self.user,
            content="This the second content."
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content="This is an answer to the first news.",
            reply=True,
            parent=self.first_news
        )

    def test_reply_this(self):
        initial_count = News.objects.count()
        self.first_news.reply_this(self.other_user, "A second answer.")
        assert News.objects.count() == initial_count + 1
        assert self.first_news.count_thread() == 2
        assert self.third_news in self.first_news.get_thread()

    def test_switch_like(self):
        self.first_news.switch_like(self.user)
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.get_likers()
