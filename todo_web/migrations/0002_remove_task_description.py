# Generated by Django 4.2.2 on 2023-06-21 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
    ]
