# Generated by Django 3.2.7 on 2022-05-25 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0004_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='crew',
        ),
    ]