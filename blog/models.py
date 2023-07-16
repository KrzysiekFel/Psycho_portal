from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from datetime import datetime


class BlogPosts(models.Model):
    title: str = models.CharField(max_length=100)
    content: str = models.TextField(blank=True)
    date_posted: datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
