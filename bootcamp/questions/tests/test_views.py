from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from bootcamp.questions.models import Question, Answer


class TestViews(TestCase):
    """
    Includes tests for all the functionality
    associated with Views
    """
    def setUp(self):
        self.client = Client()
        self.other_client = Client()
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
        self.client.login(username='test_user', password='top_secret')
        self.other_client.login(
            username='other_test_user', password='top_secret')
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

    def test_index_questions(self):
        response = self.client.get(reverse('questions'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'This is a sample question' in str(response.context['question']))

    def test_create_question_view(self):
        """
        """
        current_question_count = Question.objects.count()
        response = self.client.post(reverse('ask'),
                                    {'title': 'Not much of a title',
                                     'description': 'babla',
                                     'tags': 'test, tag'})
        self.assertEqual(response.status_code, 302)
        new_question = Question.objects.first()
        self.assertEqual(new_question.title, 'Not much of a title')
        self.assertEqual(Question.objects.count(),
                         current_question_count + 1)

    def test_answered_questions(self):
        response = self.client.get(reverse('answered'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('A Short Title' in str(response.context['question']))

    def test_all_questions_view(self):
        response = self.client.get(reverse('all'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('A Short Title' in str(response.context['question']))

    def test_individual_question(self):
        response = self.client.get(
            '/questions/{}/'.format(self.question_one.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'This is a sample question' in str(response.context['question']))

    def test_answer_question(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(
            reverse('answer'),
            {'question': self.question_one.id,
             'description': 'A reaaaaally loooong content'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Answer.objects.count(), current_answer_count + 1)

    def test_empty_answer(self):
        current_answer_count = Answer.objects.count()
        response = self.client.post(reverse('answer'),
                                    {'question': self.question_one.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Answer.objects.count(), current_answer_count)

    def test_answer_redirects(self):
        response = self.other_client.get(reverse('answer'))
        self.assertRedirects(response, reverse('questions'), status_code=302)
