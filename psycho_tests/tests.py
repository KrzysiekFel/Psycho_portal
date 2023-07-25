from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, PsychoTest, Answers
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class PsychoTestsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('psycho-tests')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.question = Question.objects.create(question_content='test_content')
        self.answers = Answers.objects.create(answers='test_answer1;test_answer2;test_answer3')
        self.test = PsychoTest.objects.create(
            name='test_name',
            description='test_description',
            threshold=1,
            result_above_threshold='test_above',
            result_below_threshold='test_below',
            author=self.user,
            answers=self.answers
        )
        self.test.questions.add(self.question)

    def test_psycho_tests_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_home.html')


class CreateTestViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('create-test')
        self.form_data = {
            'name': 'test_name',
            'description': 'test_description',
            'threshold': 5,
            'result_above_threshold': 'test_above',
            'result_below_threshold': 'test_below',
            'custom_questions': 'test_question_1\ntest_question_2',
            'answers': 'test_answer1;test_answer2;test_answer3',
        }

    def test_create_test_view_and_check_if_redirect(self):
        response = self.client.post(self.url, data=self.form_data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PsychoTest.objects.filter(name='test_name').exists())

    def test_create_test_view_and_check_if_status_200_after_redirect(self):
        response = self.client.post(self.url, data=self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(PsychoTest.objects.filter(name='test_name').exists())

    def test_check_if_template_is_used(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_create.html')


class TestViewFillResultDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('psycho-tests')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.question1 = Question.objects.create(question_content='test_content_1')
        self.question2 = Question.objects.create(question_content='test_content_2')
        self.answers = Answers.objects.create(answers='test_answer1;test_answer2;test_answer3')
        self.test = PsychoTest.objects.create(
            name='test_name',
            description='test_description',
            threshold=1,
            result_above_threshold='test_above',
            result_below_threshold='test_below',
            author=self.user,
            answers=self.answers
        )
        self.test.questions.add(self.question1, self.question2)
        self.test.answers = self.answers
        self.url = reverse('test-detail', kwargs={'test_id': self.test.id})

    def test_check_if_get_request_render_properly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_detail.html')
        self.assertContains(response, 'test_name')

    def test_check_if_post_request_render_properly(self):
        form_data = {
            'question_1': 1,
            'question_2': 2,
        }
        response = self.client.post(self.url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_result.html')
        self.assertEqual(response.context['result'].score, 3)
        self.assertContains(response, 'test_above')

    def test_check_if_results_are_correct_from_test_report(self):
        form_data = {
            'question_1': 0,
            'question_2': 0,
        }
        self.client.post(self.url, data=form_data, follow=True)
        form_data = {
            'question_1': 1,
            'question_2': 2,
        }
        self.client.post(self.url, data=form_data, follow=True)

        self.url = reverse('all-test-results')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_all_test_results.html')
        self.assertContains(response, 'test_above')
        self.assertContains(response, 'test_below')

    def test_id_test_was_correctly_deleted(self):
        self.assertTrue(PsychoTest.objects.filter(name='test_name').exists())
        self.url = reverse('delete-test', kwargs={'pk': self.test.id})

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_delete.html')

        response = self.client.delete(self.url, follow=True)
        self.assertFalse(PsychoTest.objects.filter(name='test_name').exists())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_home.html')


class PendingPsychoTestListViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setting groups
        author_group, _ = Group.objects.get_or_create(name="Author")
        publisher_group, _ = Group.objects.get_or_create(name="Publisher")
        for model in [Answers, Question, PsychoTest]:
            content_type = ContentType.objects.get_for_model(model)
            post_permission = Permission.objects.filter(content_type=content_type)
            model_delete = f"delete_{model.__name__.lower()}"
            model_change = f"change_{model.__name__.lower()}"
            for perm in post_permission:
                if perm.codename in [model_delete, model_change]:
                    publisher_group.permissions.add(perm)
                else:
                    author_group.permissions.add(perm)
                    publisher_group.permissions.add(perm)

        # setting users
        cls.user_author = User.objects.create_user(username='test_user_author', password='test_password')
        cls.user_publisher = User.objects.create_user(username='test_user_publisher', password='test_password')
        cls.user_author.groups.add(author_group)
        cls.user_publisher.groups.add(publisher_group)

        # setting tests
        cls.question1 = Question.objects.create(question_content='test_content_1')
        cls.question2 = Question.objects.create(question_content='test_content_2')
        cls.answers = Answers.objects.create(answers='test_answer1;test_answer2;test_answer3')
        cls.test_pending = PsychoTest.objects.create(
            name='test_name_pending',
            description='test_description',
            threshold=1,
            result_above_threshold='test_above',
            result_below_threshold='test_below',
            author=cls.user_author,
            answers=cls.answers
        )
        cls.test_pending.questions.add(cls.question1, cls.question2)
        cls.test_published = PsychoTest.objects.create(
            name='test_name_published',
            description='test_description',
            threshold=1,
            result_above_threshold='test_above',
            result_below_threshold='test_below',
            author=cls.user_author,
            answers=cls.answers,
            status='published'
        )
        cls.test_published.questions.add(cls.question1, cls.question2)

    def test_pending_tests_list_view_for_publisher(self):
        self.client.login(username='test_user_publisher', password='test_password')
        url = reverse('tests-to-publish')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_pending, response.context['pending_tests'])
        self.assertNotIn(self.test_published, response.context['pending_tests'])
        self.assertTemplateUsed(response, 'psycho_tests/psycho_tests_to_publish.html')
        self.assertContains(response, self.test_pending.name)
        self.assertNotContains(response, self.test_published.name)

    def test_pending_tests_list_view_for_author(self):
        self.client.login(username='test_user_author', password='test_password')
        url = reverse('tests-to-publish')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_if_pending_test_is_correctly_published(self):
        self.client.login(username='test_user_publisher', password='test_password')
        url = reverse('publish-test', args=[self.test_pending.id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('psycho-tests'))
        updated_test = PsychoTest.objects.get(id=self.test_pending.id)
        self.assertEqual(updated_test.status, "published")
