# Generated by Django 5.0.6 on 2024-05-31 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('Post_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=500)),
                ('head1', models.CharField(max_length=100)),
                ('head2', models.CharField(max_length=200)),
                ('head3', models.CharField(max_length=300)),
                ('Pub_Date', models.DateField()),
                ('thumbnail', models.ImageField(default='', upload_to='blogg/images')),
            ],
        ),
    ]
