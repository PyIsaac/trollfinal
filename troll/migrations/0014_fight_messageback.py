# Generated by Django 4.2.3 on 2024-03-01 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0013_alter_fight_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='messageback',
            field=models.TextField(default=''),
        ),
    ]
