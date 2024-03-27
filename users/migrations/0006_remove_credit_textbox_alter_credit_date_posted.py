import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_credit_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='Textbox',
        ),
        migrations.AlterField(
            model_name='credit',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]