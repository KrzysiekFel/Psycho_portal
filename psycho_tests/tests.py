from django.test import TestCase
from django.contrib.auth.models import User
from .models import Question, PsychoTest, TestResult


class QuestionModelTest(TestCase):
    def test_question_content(self):
        question = Question.objects.create(question_content='test_question')
        self.assertEqual(question.question_content, 'test_question')


class TestResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.psycho_test = PsychoTest.objects.create(
            name='Test',
            description='test_description',
            threshold=50,
            result_above_threshold='test_above',
            result_below_threshold='test_below',
            author=self.user
        )

    def test_test_result_creation(self):
        test_result = TestResult.objects.create(
            score=75,
            test=self.psycho_test,
            user=self.user
        )
        self.assertEqual(test_result.score, 75)
        self.assertEqual(test_result.test, self.psycho_test)
        self.assertEqual(test_result.user, self.user)
