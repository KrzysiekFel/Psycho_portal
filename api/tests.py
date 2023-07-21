from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from psycho_tests.models import Question, Answers, PsychoTest
from django.contrib.auth.models import User


class APIQuestionsTest(APITestCase):
    def setUp(self):
        self.url = reverse('create-questions')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.single_data = {'question_content': 'Test question 1'}
        self.many_data = [
            {'question_content': 'Test question 2'},
            {'question_content': 'Test question 3'},
        ]

    def test_question_post_method_for_one_item(self):
        response = self.client.post(self.url, self.single_data, format='json')
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_question_post_method_for_two_items(self):
        response = self.client.post(self.url, self.many_data, format='json')
        self.assertEqual(Question.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_question_get_method(self):
        Question.objects.create(question_content='Test question 1')
        Question.objects.create(question_content='Test question 2')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class APIAnswersTest(APITestCase):
    def setUp(self):
        self.url = reverse('create-answers')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.data = {'answers': 'Answer1;Answer2'}

    def test_answer_post_method(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_get_method(self):
        Answers.objects.create(answers='Answer1;Answer2')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPsychTestTest(APITestCase):
    def setUp(self):
        self.url = reverse('create-psycho-test')
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.question1 = Question.objects.create(question_content='Test question 1')
        self.question2 = Question.objects.create(question_content='Test question 2')
        self.answer = Answers.objects.create(answers='Answer1;Answer2')
        self.data = {
            'name': 'Test Name',
            'description': 'Test description',
            'threshold': 3,
            'result_above_threshold': 'Above threshold result',
            'result_below_threshold': 'Below threshold result',
            'author': self.user.id,
            'questions': [self.question1.id, self.question2.id],
            'answers': self.answer.id,
        }

    def test_psycho_test_post_methods(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PsychoTest.objects.count(), 1)

    def test_psycho_test_get_methods(self):
        self.client.post(self.url, self.data, format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
