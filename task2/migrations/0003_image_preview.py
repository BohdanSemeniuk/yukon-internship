# Generated by Django 4.1.5 on 2023-01-25 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task2', '0002_alter_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='preview',
            field=models.ImageField(null=True, upload_to='preview/'),
        ),
    ]
