# Generated by Django 4.2.3 on 2023-07-21 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_credit_aboutstart_alter_credit_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 21, 18, 23, 8, 365338, tzinfo=datetime.timezone.utc)),
        ),
    ]
