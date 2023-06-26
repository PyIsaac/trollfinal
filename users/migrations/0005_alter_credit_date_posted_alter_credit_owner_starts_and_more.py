# Generated by Django 4.1.2 on 2023-05-12 18:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_credit_date_posted_credit_daylater_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 12, 18, 25, 2, 832689, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='credit',
            name='owner_starts',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='credit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='daylater',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]