from django.urls import path
from .views import tv_shows
from core.views import scrape_data

urlpatterns = [
    path('', tv_shows, name='tv_shows'),
    path('scrape_data/', scrape_data, name='scrape_tv_shows')
]
