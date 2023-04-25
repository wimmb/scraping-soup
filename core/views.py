from django.shortcuts import render
from services import ScrapeMoviesService
from movies.models import Movie


def index(request):

    # services = ScrapeMoviesService()
    # top_movies = services.get_top_movies()

    top_movies = []
    for top_movie in top_movies:
        movie = (
            Movie.objects
            .filter(
                title=top_movie.get('title'),
                year=top_movie.get('year')
            )
            .first()
        )

        if movie:
            movie.post_image = top_movie.get('post_image')
            movie.rating = top_movie.get('rating')
            movie.save()
        else:
            movie = Movie(
                post_image=top_movie.get('post_image'),
                title=top_movie.get('title'),
                year=top_movie.get('year'),
                rating=top_movie.get('rating')
            )
            movie.save()

    return render(request, 'core/index.html')
