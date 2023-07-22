from django.db import models
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Question(models.Model):
    question_content = models.CharField(max_length=150)


class Answers(models.Model):
    answers = models.CharField(max_length=100)


class PsychoTest(models.Model):  # PsychologyTest
    date_creation = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=20)
    image = models.ImageField(default="default_test.jpg", upload_to="test_pics")
    description = models.CharField(max_length=200)
    threshold = models.IntegerField()
    result_above_threshold = models.CharField(max_length=100)
    result_below_threshold = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField("Question")
    answers = models.ForeignKey(Answers, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class TestResult(models.Model):
    score = models.IntegerField()
    date_creation = models.DateTimeField(default=timezone.now)
    test = models.ForeignKey(PsychoTest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
