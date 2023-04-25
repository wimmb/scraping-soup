from django.shortcuts import render
from .models import Movie


def top_movies(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies
    }
    return render(request, 'core/movies.html', context=context)
