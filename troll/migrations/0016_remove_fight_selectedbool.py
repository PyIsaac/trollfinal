# Generated by Django 4.2.3 on 2024-03-02 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0015_fight_selectedbool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fight',
            name='selectedbool',
        ),
    ]