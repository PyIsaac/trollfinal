# Generated by Django 4.1.2 on 2023-05-29 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_credit_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='scoreback',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 29, 17, 53, 14, 750864, tzinfo=datetime.timezone.utc)),
        ),
    ]