# Generated by Django 4.2.3 on 2023-10-17 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('troll', '0006_rename_posted_chat_chatted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='chatted',
        ),
        migrations.AddField(
            model_name='chat',
            name='should_refresh',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='chat',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]