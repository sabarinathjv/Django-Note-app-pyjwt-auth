# Generated by Django 4.0.1 on 2022-01-15 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import notes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('notes', models.TextField()),
                ('image', models.ImageField(default='posts/default.jpg', upload_to=notes.models.upload_to, verbose_name='Image')),
                ('updated_on', models.DateTimeField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]