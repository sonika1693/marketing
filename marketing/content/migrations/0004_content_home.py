# Generated by Django 3.1.7 on 2023-02-21 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_content_media_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='home',
            field=models.BooleanField(default=False),
        ),
    ]