from django.shortcuts import render
from .models import TvShows


def tv_shows(request):
    shows = TvShows.objects.all()

    context = {
        'shows': shows,
        'active_page': 'tv_shows'
    }
    return render(request, 'core/tv-shows.html', context=context)
