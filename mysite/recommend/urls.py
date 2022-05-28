from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name='recommend'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('trending', views.trending, name='trending'),
    path('displaymovie', views.displaymovie, name='displaymovie'),
    path('likedlist', views.likedlist, name='likedlist'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('watchedlist', views.watchedlist, name='watchedlist'),
    path('savedmovies', views.savedmovies, name='savedmovies'),
    path('likedmovies', views.likedmovies, name='likedmovies'),
    path('watchedmovies', views.watchedmovies, name='watchedmovies'),
    path('nav', views.watchedmovies, name='watchedmovies'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)