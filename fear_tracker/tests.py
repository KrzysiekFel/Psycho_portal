from django.test import TestCase
from .models import FearTracker
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client


class FearTrackerModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username="test_user", password="test_password")
        self.test_fear = FearTracker.objects.create(
            date="2023-01-01",
            time="00:00:00",
            activity="test_activity",
            fear_level=1,
            disturbing_thoughts="test_thoughts",
            author=self.test_user,
        )

    def test_if_str_method_shows_correct_info(self):
        self.assertEquals(
            str(self.test_fear),
            "Fear Tracker - 2023-01-01 00:00:00 - Activity: test_activity",
        )


class FearCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('fear-create')

    def test_should_redirect_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_should_return_200_when_user_logged_in_and_template_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fear_tracker/fear_tracker_form.html')

    def test_form_submission_creates_fear_tracker_object(self):
        form_data = {
            'date': '2023-01-01',
            'fear_level': 3,
            'time': '00:00:00',
            'activity': 'Test activity',
            'disturbing_thoughts': 'Test thoughts',
        }

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FearTracker.objects.filter(author=self.user, **form_data).exists())


class FearListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('fear-list')

    def test_should_return_200_when_user_logged_in_and_template_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fear_tracker/fear_tracker_list.html')


class FearDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.fear = FearTracker.objects.create(
            date="2023-01-01",
            time="00:00:00",
            activity="test_activity",
            fear_level=1,
            disturbing_thoughts="test_thoughts",
            author=self.user,
        )
        self.url = reverse('fear-delete', kwargs={'pk': self.fear.pk})

    def test_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_returns_200_for_authenticated_user_and_template_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fear_tracker/fear_tracker_delete.html')

    def test_record_is_deleted_after_confirmation(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FearTracker.objects.filter(pk=self.fear.pk).exists())


class YourChartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('fear-tracker')
        FearTracker.objects.create(
            date="2023-01-01",
            time="00:00:00",
            activity="test_activity",
            fear_level=1,
            disturbing_thoughts="test_thoughts",
            author=self.user,
        )

    def test_view_returns_200_and_context_exist(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('plot_div', response.context)
