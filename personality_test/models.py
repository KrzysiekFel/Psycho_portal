from django.db import models
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
#
# class Question(models.Model):
#     # question number
#     # question # -> TEXT FIELD
#     # answer
#     pass
#
#
# class PersonalityTest(models.Model):
#     questions = models.ManyToManyField(Question)
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)