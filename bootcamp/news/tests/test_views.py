from django.test import Client
from django.urls import reverse

from test_plus.test import TestCase

from bootcamp.news.models import News


class NewsViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
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

    def test_news_list(self):
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200
        assert self.first_news in response.context["news_list"]
        assert self.second_news in response.context["news_list"]
        assert self.third_news not in response.context["news_list"]

    def test_delete_news(self):
        initial_count = News.objects.count()
        response = self.client.post(
            reverse("news:delete_news", kwargs={"pk": self.second_news.pk}))
        assert response.status_code == 302
        assert News.objects.count() == initial_count - 1

    def test_post_news(self):
        initial_count = News.objects.count()
        response = self.client.post(
            reverse("news:post_news"), {"post": "This a third element."},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert News.objects.count() == initial_count + 1

    def test_like_news(self):
        response = self.client.post(
            reverse("news:like_post"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.get_likers()
        assert response.json()["likes"] == 1

    def test_thread(self):
        response = self.client.get(
            reverse("news:get_thread"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["uuid"] == str(self.first_news.pk)
        assert "This is a short content." in response.json()["news"]
        assert "This is an answer to the first news." in response.json()["thread"]

    def test_posting_comments(self):
        response = self.client.post(
            reverse("news:post_comments"),
            {
                "reply": "This a third element.",
                "parent": self.second_news.pk
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        assert response.json()["comments"] == 1

    def test_updating_interactions(self):
        first_response = self.client.post(
            reverse("news:like_post"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        second_response = self.other_client.post(
            reverse("news:like_post"),
            {"news": self.first_news.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        third_response = self.client.post(
            reverse("news:post_comments"),
            {
                "reply": "This a third element.",
                "parent": self.first_news.pk
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        fourth_response = self.client.post(
            reverse("news:update_interactions"),
            {"id_value": self.first_news.pk},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert first_response.status_code == 200
        assert second_response.status_code == 200
        assert third_response.status_code == 200
        assert fourth_response.status_code == 200
        assert fourth_response.json()["likes"] == 2
        assert fourth_response.json()["comments"] == 2
