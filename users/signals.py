from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from psycho_tests.models import Answers, Question, PsychoTest
from .models import Profile
from typing import Type


@receiver(post_save, sender=User)
def create_profile(sender: Type[User], instance: User, created: bool, **kwargs) -> None:
    if created:
        Profile.objects.create(user=instance)
        author_group = Group.objects.get(name="Author")
        instance.groups.add(author_group)


@receiver(post_save, sender=User)
def save_profile(sender: Type[User], instance: User, **kwargs) -> None:
    instance.profile.save()


@receiver(post_migrate)
def setup_permissions(sender, **kwargs):
    # Creates groups, only after migrating
    author_group, _ = Group.objects.get_or_create(name="Author")
    publisher_group, _ = Group.objects.get_or_create(name="Publisher")

    for model in [Answers, Question, PsychoTest]:
        content_type = ContentType.objects.get_for_model(model)
        post_permission = Permission.objects.filter(content_type=content_type)

        model_delete = f"delete_{model.__name__.lower()}"
        model_change = f"change_{model.__name__.lower()}"

        for perm in post_permission:
            if perm.codename in [model_delete, model_change]:
                publisher_group.permissions.add(perm)
            else:
                author_group.permissions.add(perm)
                publisher_group.permissions.add(perm)
