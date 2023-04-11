# Generated by Django 3.1.7 on 2023-04-11 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0014_auto_20230411_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='content',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='content.category'),
        ),
        migrations.AlterField(
            model_name='ordercontent',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.content'),
        ),
    ]
