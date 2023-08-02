from django.test import TestCase, Client
from django.urls import reverse
from .models import Profile
from django.contrib.auth.models import User


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post(self):
        form_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }

        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='test_user').exists())
        self.assertTrue(Profile.objects.filter(user__username='test_user').exists())


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.url = reverse('profile')

    def test_profile_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_view_post_valid_form(self):
        form_data = {
            'username': 'new_username',
            'email': 'newemail@example.com'
        }
        response = self.client.post(self.url, data=form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.email, 'newemail@example.com')


class UserSignalsTest(TestCase):
    def test_create_profile_signal(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_save_profile_signal(self):
        user = User.objects.create_user(username='test_user', password='test_password')
        user.username = 'new_username'
        user.save()
        self.assertTrue(Profile.objects.filter(user=user).exists())
