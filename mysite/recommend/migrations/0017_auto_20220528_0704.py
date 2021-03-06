# Generated by Django 3.2.7 on 2022-05-28 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0016_auto_20220527_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liked_movies',
            name='movie_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recommend.movie'),
        ),
        migrations.AlterField(
            model_name='saved_movies',
            name='movie_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recommend.movie'),
        ),
        migrations.AlterField(
            model_name='searched_movies',
            name='movie_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recommend.movie'),
        ),
        migrations.AlterField(
            model_name='watched_movies',
            name='movie_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recommend.movie'),
        ),
    ]
