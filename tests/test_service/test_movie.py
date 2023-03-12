from unittest.mock import MagicMock

import pytest

from app.dao.model.movie import Movie
from app.dao.movie_dao import MovieDAO
from app.service.movie_service import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie1 = Movie(id=1, title='movie1', description='movie1', trailer='trailer1',
                   year=2020, rating=5.0, genre_id=1, director_id=1)
    movie2 = Movie(id=2, title='movie2', description='movie2', trailer='trailer2',
                   year=2020, rating=5.0, genre_id=2, director_id=2)
    movie3 = Movie(id=3, title='movie3', description='movie3', trailer='trailer3',
                   year=2020, rating=5.0, genre_id=3, director_id=3)

    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.update = MagicMock(return_value=Movie(id=3))
    movie_dao.update_partial = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock(return_value=None)

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_all(self):
        data = {'status': 'new', 'page': 1}
        all_movies = self.movie_service.get_all(data)

        assert len(all_movies) == 3, 'Неверное количество фильмов'

    def test_get_one(self):
        one_movie = self.movie_service.get_one(1)

        assert one_movie.id == 1, 'Неверный фильм'
        assert one_movie.title == 'movie1', 'Неверный фильм'

    def test_create(self):
        data = {'name': 'movie4'}

        new_movie = self.movie_service.create(data)

        assert new_movie.id is not None, 'Неверный фильм'

    def test_update(self):
        data = {'name': 'movie4'}
        mid = 2

        self.movie_service.update(mid, data)

    def test_update_partial(self):
        data = {'name': 'movie4'}
        mid = 2

        self.movie_service.update(mid, data)

    def test_delete(self):
        assert self.movie_service.delete(1) is None, 'Неверный фильм'
