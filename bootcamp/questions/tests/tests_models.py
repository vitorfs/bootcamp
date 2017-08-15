from django.contrib.auth import get_user_model
from django.test import TestCase

from bootcamp.activities.models import Activity
from bootcamp.questions.models import Question


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
        self.question = Question.objects.create(
            user=self.user, title='This is a sample question',
            description='This is a sample question description',
            tags='test1,test2')

    def test_can_up_vote(self):
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question.id)
        activity.save()
        activity = Activity.objects.create(user=self.user, activity_type='U',
                                           question=self.question.id)
        activity.save()
        self.assertEqual(self.question.calculate_votes(), 2)

    def test_can_down_vote(self):
        votes = self.question.calculate_votes()
        activity = Activity.objects.create(user=self.user, activity_type='D',
                                           question=self.question.id)
        activity.save()
        self.assertEqual(self.question.calculate_votes(), votes - 1)

    def test_str_return_value(self):
        self.assertEqual(self.question, 'This is a sample question')


