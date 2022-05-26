from platform import release
from typing_extensions import runtime
from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
class Movie(models.Model):                                                                                                                                                                                                    
    genres=models.CharField(_("genres"),max_length=255)
    homepage=models.CharField(_("homepage"),max_length=255)
    movie_id=models.IntegerField(_("movie_id"))
    keywords=models.CharField(_("keywords"),max_length=255)
    original_language=models.CharField(_("original_language"),max_length=20)
    original_title=models.CharField(_("original_title"),max_length=255)
    overview=models.CharField(_("overview"),max_length=1255)
    popularity=models.FloatField(_("popularity"))
    production_countries=models.CharField(_("production_countries"),max_length=1255)
    release_date=models.DateField(_("release_date"))
    duration=models.IntegerField(_("duration"))
    spoken_language=models.CharField(_("spoken_language"),max_length=1255)
    tagline=models.CharField(_("tagline"),max_length=1255)
    title=models.CharField(_("title"),max_length=255)
    vote_average=models.FloatField(_("vote_average"))
    vote_count=models.IntegerField(_("vote_count"))
    cast=models.CharField(_("cast"),max_length=1255)
    director=models.CharField(_("director"),max_length=255)

class Liked_movies(models.Model):
    movie_id=models.ForeignKey(Movie,on_delete=models.CASCADE)
    liked=models.BooleanField(default=False)
class Watched_movies(models.Model):
    movie_id=models.ForeignKey(Movie,on_delete=models.CASCADE)
    watched=models.BooleanField(default=False)
class Searched_movies(models.Model):
    movie_id=models.ForeignKey(Movie,on_delete=models.CASCADE)
    searched=models.BooleanField(default=False)







                                                                                                                                                     
