# Generated by Django 4.2.5 on 2023-11-26 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_userbook_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
    ]
