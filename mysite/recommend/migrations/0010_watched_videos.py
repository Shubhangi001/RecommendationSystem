# Generated by Django 3.2.7 on 2022-05-26 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0009_liked_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watched_videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.movie')),
            ],
        ),
    ]