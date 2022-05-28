from django.contrib import admin
from . import models
# from .models import Movie,Saved_movies,Watched_movies,Searched_movies,Liked_movies,
# Register your models here.
admin.site.register(models.Movie)
admin.site.register(models.Watched_movies)
admin.site.register(models.Searched_movies)
admin.site.register(models.Liked_movies)
admin.site.register(models.Saved_movies)