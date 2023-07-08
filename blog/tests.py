from django.test import TestCase
from .models import BlogPosts
from django.urls import reverse
from django.contrib.auth.models import User


class BlogPostModelTest(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_user', password='test_password')
        self.test_post = BlogPosts.objects.create(title='test_title', content='test_content', author=test_user)

    def test_if_str_method_shows_title(self):
        self.assertEquals(str(self.test_post), 'test_title')


class AboutViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('about'))

    def test_about_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'about.html')

