from django.contrib.auth import get_user_model
from django.test import TestCase

from bootcamp.activities.models import Activity, Notification
from bootcamp.articles.models import Article
from bootcamp.feeds.models import Feed
from bootcamp.questions.models import Question, Answer


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
        self.feed = Feed.objects.create(
            user=self.user,
            post='A not so long text',
            likes=0,
            comments=0
        )
        self.question = Question.objects.create(
            user=self.user,
            title='A Short Title',
            description='A reaaaaally loooong content',
            favorites=0,
            has_accepted_answer=True
        )
        self.answer = Answer.objects.create(
            user=self.user,
            question=self.question,
            description='A reaaaaally loooong content',
            votes=0,
            is_accepted=True
        )
        self.article = Article.objects.create(
            title='A really nice title',
            content='This is a really good content',
            status='P',
            create_user=self.user,
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

    def test_register_fav_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='F'
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(str(activity), 'F')
        self.assertNotEqual(str(activity), 'f')

    def test_register_like_activity(self):
        activity = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        self.assertTrue(isinstance(activity, Activity))
        self.assertEqual(str(activity), 'L')

    def test_activity_daily_statistic(self):
        activity_one = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        activity_two = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        activity_three = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        self.assertTrue(isinstance(activity_one, Activity))
        self.assertTrue(isinstance(activity_two, Activity))
        self.assertTrue(isinstance(activity_three, Activity))
        self.assertEqual(Activity.daily_activity(self.user), ('[{}]'.format(
            Activity.objects.all().count()), '["{}"]'.format(
                activity_one.date.date())))
        self.assertEqual(Activity.daily_activity(self.other_user)[0], '0')

    def test_activity_monthly_statistic(self):
        activity_one = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        activity_two = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        activity_three = Activity.objects.create(
            user=self.user,
            activity_type='L'
        )
        self.assertTrue(isinstance(activity_one, Activity))
        self.assertTrue(isinstance(activity_two, Activity))
        self.assertTrue(isinstance(activity_three, Activity))
        self.assertEqual(Activity.monthly_activity(self.user)[0],
                         '[{}]'.format(Activity.objects.all().count()))
        self.assertEqual(Activity.monthly_activity(self.other_user)[0], '0')

    def test_register_like_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='L',
            is_read=False
        )
        test_string = notification._LIKED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.feed.pk, notification.get_summary(self.feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'l')

    def test_register_comm_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='C',
            is_read=False
        )
        test_string = notification._COMMENTED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.feed.pk, notification.get_summary(self.feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'c')

    def test_register_fav_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            question=self.question,
            notification_type='F',
            is_read=False
        )
        test_string = notification._FAVORITED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.question.pk, notification.get_summary(self.question.title))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'f')

    def test_register_answered_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            question=self.question,
            notification_type='A',
            is_read=False
        )
        test_string = notification._ANSWERED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.question.pk, notification.get_summary(self.question.title))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'a')

    def test_register_accepted_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            question=self.question,
            answer=self.answer,
            notification_type='W',
            is_read=False
        )
        test_string = notification._ACCEPTED_ANSWER_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.answer.question.pk, notification.get_summary(
                self.answer.description))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'w')

    def test_register_also_comm_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='S',
            is_read=False
        )
        test_string = notification._ALSO_COMMENTED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.feed.pk, notification.get_summary(self.feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 's')

    def test_return_sumary(self):
        feed = Feed.objects.create(
            user=self.user,
            post='kjahsdfklahsdlklsdjflakjnzxcvzmncx.vmznxcvlheiruyweihlkdfklajdflk hasldjhalksdfh jklhljk',  # noqa: E501
            likes=0,
            comments=0
        )
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=feed,
            notification_type='L',
            is_read=False
        )
        test_string = notification._LIKED_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            feed.pk, notification.get_summary(feed.post))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'l')

    def test_register_else_notification(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='Z',
            is_read=False
        )
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), 'Ooops! Something went wrong.')
        self.assertNotEqual(str(notification), 'z')

    def test_register_edited_article(self):
        notification = Notification.objects.create(
            from_user=self.user,
            to_user=self.other_user,
            feed=self.feed,
            notification_type='E',
            article=self.article,
            is_read=False
        )
        test_string = notification._EDITED_ARTICLE_TEMPLATE.format(
            self.user.username, self.user.profile.get_screen_name(),
            self.article.slug, notification.get_summary(self.article.title))
        self.assertTrue(isinstance(notification, Notification))
        self.assertEqual(str(notification), test_string)
        self.assertNotEqual(str(notification), 'e')
