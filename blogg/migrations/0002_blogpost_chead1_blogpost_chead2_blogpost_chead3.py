# Generated by Django 5.0.6 on 2024-05-31 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='Chead1',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='Chead2',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='Chead3',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
