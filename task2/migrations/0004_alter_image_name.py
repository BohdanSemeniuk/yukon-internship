# Generated by Django 4.1.5 on 2023-01-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0003_image_preview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
