from django.db import models
from django.contrib.auth.models import User
from typing import List, Tuple

ANXIETY_CHOICES: List[Tuple[int, str]] = [
    (1, 'Minimal anxiety'),
    (2, 'Mild anxiety'),
    (3, 'Moderate anxiety'),
    (4, 'Intense anxiety'),
    (5, 'Severe anxiety'),
]


class FearTracker(models.Model):
    date = models.DateField()
    time = models.TimeField()
    activity = models.CharField(max_length=100, blank=True)
    fear_level = models.IntegerField(choices=ANXIETY_CHOICES)
    disturbing_thoughts = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fear Tracker - {self.date} {self.time} - Activity: {self.activity}"
