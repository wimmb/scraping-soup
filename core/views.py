from django.shortcuts import render
from services import ScrapeMoviesService, ScrapeTvShowsService
from movies.models import Movie
from tv_shows.models import TvShows


def index(request):

    services_m = ScrapeMoviesService()
    top_movies = services_m.get_top_movies()

    # top_movies = []
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

    services_tv = ScrapeTvShowsService()
    tv_shows = services_tv.get_tv_shows()

    # tv_shows = []
    for tv_show in tv_shows:
        show = (
            TvShows.objects
            .filter(
                title=tv_show.get('title'),
                year=tv_show.get('year')
            )
            .first()
        )

        if show:
            show.post_image = tv_show.get('post_image')
            show.rating = tv_show.get('rating')
            show.save()
        else:
            show = TvShows(
                post_image=tv_show.get('post_image'),
                title=tv_show.get('title'),
                year=tv_show.get('year'),
                rating=tv_show.get('rating')
            )
            show.save()

    context = {
        'active_page': 'home'
    }

    return render(request, 'core/index.html', context=context)
