# Generated by Django 4.2.3 on 2024-02-29 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0012_fight_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fight',
            name='selected',
            field=models.IntegerField(default=0),
        ),
    ]
