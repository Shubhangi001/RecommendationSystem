# Generated by Django 3.2.7 on 2022-05-27 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0011_auto_20220526_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liked_movies',
            name='liked',
        ),
    ]
