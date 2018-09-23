from test_plus.test import TestCase

from bootcamp.qa.models import Question, Answer


class QAModelsTest(TestCase):
    def setUp(self):
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
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

    def test_can_vote_question(self):
        self.question_one.votes.update_or_create(
            user=self.user, defaults={"value": True}, )
        self.question_one.votes.update_or_create(
            user=self.other_user, defaults={"value": True})
        self.question_one.count_votes()
        assert self.question_one.total_votes == 2

    def test_can_vote_answer(self):
        self.answer.votes.update_or_create(
            user=self.user, defaults={"value": True}, )
        self.answer.votes.update_or_create(
            user=self.other_user, defaults={"value": True}, )
        self.answer.count_votes()
        assert self.answer.total_votes == 2

    def test_get_question_voters(self):
        self.question_one.votes.update_or_create(
            user=self.user, defaults={"value": True}, )
        self.question_one.votes.update_or_create(
            user=self.other_user, defaults={"value": False})
        self.question_one.count_votes()
        assert self.user in self.question_one.get_upvoters()
        assert self.other_user in self.question_one.get_downvoters()

    def test_get_answern_voters(self):
        self.answer.votes.update_or_create(
            user=self.user, defaults={"value": True}, )
        self.answer.votes.update_or_create(
            user=self.other_user, defaults={"value": False})
        self.answer.count_votes()
        assert self.user in self.answer.get_upvoters()
        assert self.other_user in self.answer.get_downvoters()

    def test_question_str_return_value(self):
        assert isinstance(self.question_one, Question)
        assert str(self.question_one) == "This is a sample question"

    def test_question_non_answered_question(self):
        assert self.question_one == Question.objects.get_unanswered()[0]

    def test_question_answered_question(self):
        assert self.question_two == Question.objects.get_answered()[0]

    def test_question_answers_returns(self):
        assert self.answer == self.question_two.get_answers()[0]

    def test_question_answer_count(self):
        assert self.question_two.count_answers == 1

    def test_question_accepted_answer(self):
        assert self.question_two.get_accepted_answer() == self.answer

    # Answer model tests
    def test_answer_return_value(self):
        assert str(self.answer) == "A reaaaaally loooong content"

    def test_answer_accept_method(self):
        answer_one = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="A reaaaaally loooonger content"
        )
        answer_two = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="A reaaaaally even loooonger content"
        )
        answer_three = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            content="Even a reaaaaally loooonger content"
        )
        self.assertFalse(answer_one.is_answer)
        self.assertFalse(answer_two.is_answer)
        self.assertFalse(answer_three.is_answer)
        self.assertFalse(self.question_one.has_answer)
        answer_one.accept_answer()
        self.assertTrue(answer_one.is_answer)
        self.assertFalse(answer_two.is_answer)
        self.assertFalse(answer_three.is_answer)
        self.assertTrue(self.question_one.has_answer)
        self.assertEqual(self.question_one.get_accepted_answer(), answer_one)
