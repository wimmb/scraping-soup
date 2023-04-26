from django.urls import path
from .views import tv_shows


urlpatterns = [
    path('tv-shows/', tv_shows, name='tv_shows')
]
