from django.contrib import admin
from .models import Movie,Watched_movies,Searched_movies
# Register your models here.
admin.site.register(Movie)
admin.site.register(Watched_movies)
admin.site.register(Searched_movies)