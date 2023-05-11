from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
import configs
from movies.models import Movie
from django.forms.models import model_to_dict

from tv_shows.models import TvShows


class IMDBService:

    MOVIES = 'movies'
    TV_SHOWS = 'tv_shows'
    url = ''
    parser_count = 0

    def get_objects(self):

        if not self.url or self.parser_count == 0:
            raise ValueError

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        poster_tags = soup.find_all('td', class_="posterColumn")
        title_tags = soup.find_all('td', class_="titleColumn")
        rating_tags = soup.find_all('td', class_="ratingColumn imdbRating")

        assert len(poster_tags) == len(title_tags) == len(rating_tags) == self.parser_count, 'Error'

        results = []
        for i in range(len(poster_tags)):
            post_image = self.parse_poster_image(tag=poster_tags[i])
            title = self.parse_title(tag=title_tags[i])
            year = self.parse_year(tag=title_tags[i])
            rating = self.parse_rating(tag=rating_tags[i])

            results.append(
                {
                    'post_image': post_image,
                    'title': title,
                    'year': year,
                    'rating': rating
                }
            )
        return results

    def persist_objects(self, objects):
        raise NotImplementedError

    @classmethod
    def get_service(cls, category):
        if category == cls.MOVIES:
            return ScrapeMoviesService()
        elif category == cls.TV_SHOWS:
            return ScrapeTvShowsService()
        else:
            raise NotImplementedError

    def parse_poster_image(self, tag):
        return tag.find('img')['src']

    def parse_title(self, tag):
        return tag.find('a').text

    def parse_year(self, tag):
        return int(tag.find('span', class_="secondaryInfo").text.lstrip('(').rstrip(')').strip())

    def parse_rating(self, tag):
        rating = tag.find('strong')
        if rating is None:
            return float(0)
        return float(rating.text.strip())


class ScrapeMoviesService(IMDBService):

    url = 'https://www.imdb.com/chart/top'
    parser_count = 250

    def persist_objects(self, objects):
        movies = []

        for top_movie in objects:
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
            movies.append(model_to_dict(movie))
        return movies


class ScrapeTvShowsService(IMDBService):

    url = 'https://www.imdb.com/chart/tvmeter'
    parser_count = 100

    def persist_objects(self, objects):
        tv_shows = []

        for tv_show in objects:
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
            tv_shows.append(model_to_dict(show))
        return tv_shows


if __name__ == '__main__':
    # top movies
    service_movies = IMDBService.get_service(category=IMDBService.MOVIES)
    top_movies = service_movies.get_objects()

    df = pd.DataFrame.from_dict(top_movies)

    output_file_path = Path(configs.basedir) / 'movies.csv'
    df.to_csv(output_file_path)

    # tv shows
    service_shows = IMDBService.get_service(category=IMDBService.TV_SHOWS)
    tv_shows = service_shows.get_objects()

    df = pd.DataFrame.from_dict(tv_shows)

    output_file_path = Path(configs.basedir) / 'tv_shows.csv'
    df.to_csv(output_file_path)
