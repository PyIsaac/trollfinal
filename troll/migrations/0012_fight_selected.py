# Generated by Django 4.2.3 on 2024-02-27 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0011_fight_user_alter_fight_matchfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]