# Generated by Django 4.1.2 on 2023-06-10 18:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_credit_scorebackreal_alter_credit_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 10, 18, 9, 7, 438180, tzinfo=datetime.timezone.utc)),
        ),
    ]
