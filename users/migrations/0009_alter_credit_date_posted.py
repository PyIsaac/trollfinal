# Generated by Django 4.1.2 on 2023-05-27 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_credit_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 27, 18, 30, 45, 919896, tzinfo=datetime.timezone.utc)),
        ),
    ]
