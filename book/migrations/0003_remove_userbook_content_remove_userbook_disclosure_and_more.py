# Generated by Django 4.2.5 on 2023-11-21 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbook',
            name='content',
        ),
        migrations.RemoveField(
            model_name='userbook',
            name='disclosure',
        ),
        migrations.AddField(
            model_name='userbook',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
