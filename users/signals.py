from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from typing import Type


@receiver(post_save, sender=User)
def create_profile(sender: Type[User], instance: User, created: bool, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender: Type[User], instance: User, **kwargs) -> None:
    instance.profile.save()
