# Generated by Django 4.2.3 on 2024-03-16 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troll', '0016_remove_fight_selectedbool'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='secondredir',
            field=models.BooleanField(default=False),
        ),
    ]