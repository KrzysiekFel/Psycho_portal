# Generated by Django 4.2.2 on 2023-07-08 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personality_test', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_content', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='PsychoTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(default='default_test.jpg', upload_to='test_pics')),
                ('description', models.CharField(max_length=200)),
                ('threshold', models.IntegerField()),
                ('result_above_threshold', models.CharField(max_length=100)),
                ('result_below_threshold', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('questions', models.ManyToManyField(to='personality_test.question')),
            ],
        ),
    ]