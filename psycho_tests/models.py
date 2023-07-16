from django.db import models
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Question(models.Model):
    question_content: str = models.CharField(max_length=150)


class PsychoTest(models.Model):
    date_creation: datetime = models.DateTimeField(default=timezone.now)
    name: str = models.CharField(max_length=20)
    image = models.ImageField(default="default_test.jpg", upload_to="test_pics")
    description: str = models.CharField(max_length=200)
    threshold: int = models.IntegerField()
    result_above_threshold: str = models.CharField(max_length=100)
    result_below_threshold: str = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Answer(models.Model):
    answer: str = models.CharField(max_length=50)
    psycho_test = models.ForeignKey(PsychoTest, related_name='answers', on_delete=models.CASCADE)


class TestResult(models.Model):
    score: int = models.IntegerField()
    date_creation: datetime = models.DateTimeField(default=timezone.now)
    test = models.ForeignKey(PsychoTest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
