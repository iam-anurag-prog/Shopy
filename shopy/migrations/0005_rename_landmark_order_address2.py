# Generated by Django 5.0.6 on 2024-05-29 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopy', '0004_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='landmark',
            new_name='address2',
        ),
    ]
