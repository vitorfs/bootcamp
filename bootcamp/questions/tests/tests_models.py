from django.contrib.auth.models import User
from django.test import TestCase

from bootcamp.activities.models import Activity
from bootcamp.questions.models import Question


class QuestionVoteTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword',
                                        email='testuser@example.com')
        question = Question.objects.create(user=user,
                                           title='This is a sample question',
                                           description='This is a sample question description',
                                           tags='test1,test2')

    def test_can_up_vote(self):
        question = Question.objects.get(title__exact='This is a sample question')
        activity = Activity.objects.create(user=User.objects.get(username='testuser'),
                                           activity_type='U',
                                           question=question.id)
        activity.save()
        activity = Activity.objects.create(user=User.objects.get(username='testuser'),
                                           activity_type='U',
                                           question=question.id)
        activity.save()
        self.assertEqual(question.calculate_votes(), 2)

    def test_can_down_vote(self):
        question = Question.objects.get(title__exact='This is a sample question')
        votes = question.calculate_votes()
        activity = Activity.objects.create(user=User.objects.get(username='testuser'),
                                           activity_type='D',
                                           question=question.id)
        activity.save()
        self.assertEqual(question.calculate_votes(), votes - 1)
