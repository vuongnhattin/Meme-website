# Generated by Django 5.0.3 on 2024-03-07 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_submittedfile_image_submittedfile_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='SubmittedFile',
        ),
    ]