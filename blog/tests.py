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


class BlogPostListTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='test_password')
        self.blog_post = BlogPosts.objects.create(title='Test Post', content='Test content', author=self.test_user)
        self.response = self.client.get(reverse('blog-posts'))

    def test_about_view_and_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/home.html')


class BlogPostDetailTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user', password='test_password')
        self.blog_post = BlogPosts.objects.create(title='Test Post', content='Test content', author=self.test_user)

    def test_view_returns_200_for_existing_post(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': self.blog_post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_404_for_nonexistent_post(self):
        response = self.client.get(reverse('post-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
