# Generated by Django 3.1.7 on 2023-04-03 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_content_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]