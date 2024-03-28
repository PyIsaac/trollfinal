# Generated by Django 4.2.3 on 2023-09-05 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('troll', '0002_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chat',
            name='content',
            field=models.TextField(default=''),
        ),
    ]