from django.db import models
from PIL import Image
from django.utils import timezone
from django.contrib.auth.models import User

CHOICES = [(1, 1),
           (2, 2)]


class PersonalityTest(models.Model):
    question_1 = models.IntegerField(choices=CHOICES)
    question_2 = models.IntegerField(choices=CHOICES)
    question_3 = models.IntegerField(choices=CHOICES)
    question_4 = models.IntegerField(choices=CHOICES)
    question_5 = models.IntegerField(choices=CHOICES)
    question_6 = models.IntegerField(choices=CHOICES)
    question_7 = models.IntegerField(choices=CHOICES)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    question_content = models.CharField(max_length=150)


class PsychoTest(models.Model):
    date_creation = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=20)
    image = models.ImageField(default="default_test.jpg", upload_to="test_pics")
    description = models.CharField(max_length=200)
    threshold = models.IntegerField()
    result_above_threshold = models.CharField(max_length=100)
    result_below_threshold = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
