from django.test import Client
from django.urls import reverse

from test_plus.test import TestCase

from bootcamp.qa.models import Question, Answer


class QAViewsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("first_user")
        self.other_user = self.make_user("second_user")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username="first_user", password="password")
        self.other_client.login(username="second_user", password="password")
        self.question_one = Question.objects.create(
            user=self.user, title="This is a sample question",
            content="This is a sample question content",
            tags="test1, test2"
        )
        self.question_two = Question.objects.create(
            user=self.user,
            title="A Short Title",
            content="""This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.""",
            has_answer=True,
            tags="test1, test2"
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            content="A reaaaaally loooong content",
            is_answer=True
        )

    def test_index_questions(self):
        response = self.client.get(reverse("qa:index_all"))
        assert response.status_code == 200
        assert "A Short Title" in str(response.context["question"])

    def test_create_question_view(self):
        current_count = Question.objects.count()
        response = self.client.post(reverse("qa:ask_question"),
                                    {"title": "Not much of a title",
                                     "content": "bablababla bablababla",
                                     "status": "O",
                                     "tags": "test, tag"})
        assert response.status_code == 302
        new_question = Question.objects.first()
        assert new_question.title == "Not much of a title"
        assert Question.objects.count() == current_count + 1

    def test_answered_questions(self):
        response = self.client.get(reverse("qa:index_ans"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("A Short Title" in str(response.context["question"]))

    def test_unanswered_questions(self):
        response = self.client.get(reverse("qa:index_noans"))
        assert response.status_code == 200
        assert "This is a sample question" in str(response.context["question"])

    def test_answer_question(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse("qa:propose_answer",
                    kwargs={"question_id": self.question_one.id}),
            {"content": "A reaaaaally loooong content"}
        )
        assert response.status_code == 302
        assert Answer.objects.count() == current_answer_count + 1

    def test_question_upvote(self):
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "U", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_question_downvote(self):
        response_one = self.client.post(
            reverse("qa:question_vote"),
            {"value": "D", "question": self.question_one.id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_upvote(self):
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "U", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_answer_downvote(self):
        response_one = self.client.post(
            reverse("qa:answer_vote"),
            {"value": "D", "answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200

    def test_accept_answer(self):
        response_one = self.client.post(
            reverse("qa:accept_answer"),
            {"answer": self.answer.uuid_id},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response_one.status_code == 200
