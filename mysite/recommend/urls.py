from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name='recommend'
urlpatterns = [
    path('', views.index, name='index'),
    path('displaymovie', views.displaymovie, name='displaymovie'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)