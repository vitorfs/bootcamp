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

    def test_can_up_vote_question(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question_one.id)
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question_one.id)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.question_one.calculate_votes(), 2)

    def test_can_down_vote_question(self):
        votes = self.question_one.calculate_votes()
        activity = Activity.objects.create(user=self.user, activity_type='D',
                                           question=self.question_one.id)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.question_one.calculate_votes(), votes - 1)

    def test_question_str_return_value(self):
        self.assertTrue(isinstance(self.question_one, Question))
        self.assertEqual(str(self.question_one), 'This is a sample question')

    def test_question_non_answered_question(self):
        self.assertEqual(self.question_one, Question.get_unanswered()[0])

    def test_question_answered_question(self):
        self.assertEqual(self.question_two, Question.get_answered()[0])

    def test_question_answers_returns(self):
        self.assertEqual(self.answer, self.question_two.get_answers()[0])

    def test_question_answer_count(self):
        self.assertEqual(self.question_two.get_answers_count(), 1)

    def test_question_accepted_answer(self):
        self.assertEqual(self.question_two.get_accepted_answer(), self.answer)

    def test_question_markdown_return(self):
        self.assertEqual(self.question_one.get_description_as_markdown(),
                         '<p>This is a sample question description</p>')
        self.assertEqual(self.question_two.get_description_as_markdown(),
                         '''<p>This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a test;
            everybody always wants the real deal.</p>''')

    def test_question_return_summary(self):
        self.assertEqual(len(self.question_two.get_description_preview()), 258)
        self.assertEqual(self.question_two.get_description_preview(),
                         '''This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a te...''')
        self.assertEqual(self.question_one.get_description_preview(),
                         'This is a sample question description')

    def test_question_markdown_description_preview(self):
        self.assertTrue(
            self.question_two.get_description_preview_as_markdown(),
            '''<p>This is a really good content, just if somebody
            published it, that would be awesome, but no, nobody wants to
            publish it, because they know this is just a test, and you
            know than nobody wants to publish a test, just a te...</p>''')

    def test_favorite_question(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='F',
            question=self.question_one.id
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.question_one.calculate_favorites(), 1)

    def test_question_favoriters(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='F',
            question=self.question_one.id
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.user, self.question_one.get_favoriters()[0].user)

    def test_question_voters_retun_values(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question_one.id)
        activity = Activity.objects.create(user=self.other_user,
                                           activity_type='D',
                                           question=self.question_one.id)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.question_one.get_up_voters()[0].user, self.user)
        self.assertEqual(
            self.question_one.get_down_voters()[0].user, self.other_user)

    # Answer model tests
    def test_answer_return_value(self):
        self.assertEqual(str(self.answer), 'A reaaaaally loooong content')

    def test_answer_accept_method(self):
        answer_one = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            description='A reaaaaally loooonger content'
        )
        answer_two = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            description='A reaaaaally even loooonger content'
        )
        answer_three = Answer.objects.create(
            user=self.user,
            question=self.question_one,
            description='Even a reaaaaally loooonger content'
        )
        self.assertFalse(answer_one.is_accepted)
        self.assertFalse(answer_two.is_accepted)
        self.assertFalse(answer_three.is_accepted)
        self.assertFalse(self.question_one.has_accepted_answer)
        answer_one.accept()
        self.assertTrue(answer_one.is_accepted)
        self.assertFalse(answer_two.is_accepted)
        self.assertFalse(answer_three.is_accepted)
        self.assertTrue(self.question_one.has_accepted_answer)
        self.assertEqual(self.question_one.get_accepted_answer(), answer_one)

    def test_answers_vote_calculation(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           answer=self.answer.id)
        activity = Activity.objects.create(user=self.other_user,
                                           activity_type='U',
                                           answer=self.answer.id)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.answer.calculate_votes(), 2)

    def test_answer_voters_return_values(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           answer=self.answer.id)
        activity = Activity.objects.create(user=self.other_user,
                                           activity_type='D',
                                           answer=self.answer.id)
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(self.answer.get_up_voters()[0].user, self.user)
        self.assertEqual(
            self.answer.get_down_voters()[0].user, self.other_user)

    def test_answer_description_markdown(self):
        self.assertEqual(self.answer.get_description_as_markdown(),
                         '<p>A reaaaaally loooong content</p>')
