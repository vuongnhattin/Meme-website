# Generated by Django 5.0.3 on 2024-03-06 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
    ]
