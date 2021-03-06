# Generated by Django 3.2.7 on 2022-05-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genres', models.CharField(max_length=255, verbose_name='genres')),
                ('homepage', models.CharField(max_length=255, verbose_name='homepage')),
                ('movie_id', models.IntegerField(verbose_name='movie_id')),
                ('keywords', models.CharField(max_length=255, verbose_name='keywords')),
                ('original_language', models.CharField(max_length=20, verbose_name='original_language')),
                ('original_title', models.CharField(max_length=255, verbose_name='original_title')),
                ('overview', models.CharField(max_length=1255, verbose_name='overview')),
                ('popularity', models.FloatField(verbose_name='popularity')),
                ('release_date', models.DateField(verbose_name='release_date')),
                ('duration', models.IntegerField(verbose_name='duration')),
                ('tagline', models.CharField(max_length=1255, verbose_name='tagline')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('vote_average', models.FloatField(verbose_name='vote_average')),
                ('cast', models.CharField(max_length=255, verbose_name='cast')),
                ('director', models.CharField(max_length=255, verbose_name='director')),
            ],
        ),
    ]
