# Generated by Django 3.2.7 on 2022-05-25 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0006_remove_movie_revenue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='budget',
        ),
    ]
