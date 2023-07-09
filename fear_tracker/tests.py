import datetime
from django.test import TestCase, RequestFactory
from .views import YourChartView
from .forms import FearTrackerForm
from .models import FearTracker
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client


class FearTrackerModelTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_user', password='test_password')
        self.test_fear = FearTracker.objects.create(
            date='2023-01-01',
            time='00:00:00',
            activity='test_activity',
            fear_level=1,
            disturbing_thoughts='test_thoughts',
            author=test_user)

    def test_if_str_method_shows_correct_info(self):
        self.assertEquals(str(self.test_fear), 'Fear Tracker - 2023-01-01 00:00:00 - Activity: test_activity')


class FearTrackerViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username='test_user', password='test_password')
        self.response = self.client.get('/fear_tracker/')

    def test_if_correct_response_for_fear_tracker(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Fear Tracker')
        self.assertTemplateUsed(self.response, 'fear_tracker/fear_tracker.html')


class FearCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.test_form_data = {
            'date': '2023-01-01',
            'time': '00:00:00',
            'activity': 'test_activity',
            'fear_level': 1,
            'disturbing_thoughts': 'test_thoughts',
            'author': self.test_user}

    def test_if_form_is_valid(self):
        form = FearTrackerForm(data=self.test_form_data)
        response = self.client.post(reverse('fear-create'), data=self.test_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 302)


class YourChartViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.fear_tracker_1 = FearTracker.objects.create(
            date=datetime.date(2023, 1, 1),
            time=datetime.time(12, 0, 0),
            activity='Test Activity 1',
            fear_level=2,
            disturbing_thoughts='Test Thoughts 1',
            author=self.user
        )
        self.fear_tracker_2 = FearTracker.objects.create(
            date=datetime.date(2023, 1, 2),
            time=datetime.time(14, 0, 0),
            activity='Test Activity 2',
            fear_level=4,
            disturbing_thoughts='Test Thoughts 2',
            author=self.user
        )

    def test_if_data_are_correct(self):
        request = self.factory.get(reverse('fear-plot'))
        request.user = self.user
        view = YourChartView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chart of your anxiety level')
        self.assertContains(response, '<div class="plot-container">')
        self.assertIn('plot_div', response.context_data)
        self.assertIsInstance(response.context_data['plot_div'], str)