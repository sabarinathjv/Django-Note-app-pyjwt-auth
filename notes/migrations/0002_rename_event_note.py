# Generated by Django 4.0.1 on 2022-01-15 13:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Note',
        ),
    ]
