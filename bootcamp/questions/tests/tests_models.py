from django.contrib.auth import get_user_model
from django.test import TestCase

from bootcamp.activities.models import Activity
from bootcamp.questions.models import Question, Answer


class QuestionVoteTest(TestCase):
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
        self.question_one = Question.objects.create(
            user=self.user, title='This is a sample question',
            description='This is a sample question description',
            tags='test1,test2')
        self.question_two = Question.objects.create(
            user=self.user,
            title='A Short Title',
            description='''This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.''',
            favorites=0,
            has_accepted_answer=True
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question_two,
            description='A reaaaaally loooong content',
            votes=0,
            is_accepted=True
        )

    def test_can_up_vote(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question_one.id)
        activity.save()
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question_one.id)
        activity.save()
        self.assertEqual(self.question_one.calculate_votes(), 2)

    def test_can_down_vote(self):
        votes = self.question_one.calculate_votes()
        activity = Activity.objects.create(user=self.user, activity_type='D',
                                           question=self.question_one.id)
        activity.save()
        self.assertEqual(self.question_one.calculate_votes(), votes - 1)

    def test_str_return_value(self):
        self.assertTrue(isinstance(self.question_one, Question))
        self.assertEqual(str(self.question_one), 'This is a sample question')

    def test_non_answered_question(self):
        self.assertEqual(self.question_one, Question.get_unanswered()[0])

    def test_answered_question(self):
        self.assertEqual(self.question_two, Question.get_answered()[0])

    def test_answers_returns(self):
        self.assertEqual(self.answer, self.question_two.get_answers()[0])

    def test_answer_count(self):
        self.assertEqual(self.question_two.get_answers_count(), 1)

    def test_accepted_answer(self):
        self.assertEqual(self.question_two.get_accepted_answer(), self.answer)

    def test_markdown_return(self):
        self.assertEqual(self.question_one.get_description_as_markdown(),
                         '<p>This is a sample question description</p>')
        self.assertEqual(self.question_two.get_description_as_markdown(),
                         '''<p>This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.</p>''')

    def test_return_summary(self):
        self.assertEqual(len(self.question_two.get_description_preview()), 258)
        self.assertEqual(self.question_two.get_description_preview(),
                         '''This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a te...''')
