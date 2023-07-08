from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTest(TestCase):
    def test_if_registration_works_properly(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse('register'), data=data)
        self.assertEquals(response.status_code, 302)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_if_profile_works_properly(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['user_form']
        self.assertFalse(form.is_valid())
        form = response.context['profile_form']
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse('profile'), data=data)
        self.assertEquals(response.status_code, 302)
