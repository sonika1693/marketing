# Generated by Django 3.1.7 on 2023-04-11 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20230410_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_id',
            new_name='txn_id',
        ),
    ]
