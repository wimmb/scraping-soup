from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
import configs


class ScrapeMoviesService:

    url = 'https://www.imdb.com/chart/top'
    parser_count = 250

    def get_tops(self):

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


class ScrapeTvShowsService(ScrapeMoviesService):

    url = 'https://www.imdb.com/chart/tvmeter'
    parser_count = 100


if __name__ == '__main__':
    # top movies
    service_movies = ScrapeMoviesService()
    top_movies = service_movies.get_tops()

    df = pd.DataFrame.from_dict(top_movies)

    output_file_path = Path(configs.basedir) / 'movies.csv'
    df.to_csv(output_file_path)

    # tv shows
    service_shows = ScrapeTvShowsService()
    tv_shows = service_shows.get_tops()

    df = pd.DataFrame.from_dict(tv_shows)

    output_file_path = Path(configs.basedir) / 'tv_shows.csv'
    df.to_csv(output_file_path)
