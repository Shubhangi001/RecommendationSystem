from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Movie)
admin.site.register(models.Watched_movies)
admin.site.register(models.Searched_movies)
admin.site.register(models.Liked_movies)
admin.site.register(models.Saved_movies)