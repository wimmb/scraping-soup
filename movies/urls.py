from django.urls import path
from .views import top_movies
from core.views import scrape_data

urlpatterns = [
    path('', top_movies, name='movies'),
    path('scrape_data/', scrape_data, name='scrape_movies')
]
