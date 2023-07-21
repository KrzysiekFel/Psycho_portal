from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, PsychoTest, Answers


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
