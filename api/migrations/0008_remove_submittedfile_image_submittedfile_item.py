# Generated by Django 5.0.3 on 2024-03-07 04:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_item_image_submittedfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submittedfile',
            name='image',
        ),
        migrations.AddField(
            model_name='submittedfile',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.item'),
            preserve_default=False,
        ),
    ]