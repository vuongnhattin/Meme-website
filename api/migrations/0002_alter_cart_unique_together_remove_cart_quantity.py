# Generated by Django 5.0.3 on 2024-03-05 16:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'item')},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
    ]
