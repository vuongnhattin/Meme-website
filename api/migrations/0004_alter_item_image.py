# Generated by Django 5.0.3 on 2024-03-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='fallback.png', upload_to=''),
        ),
    ]
