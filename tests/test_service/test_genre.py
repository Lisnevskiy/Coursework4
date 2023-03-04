from unittest.mock import MagicMock

import pytest

from app.dao.model.genre import Genre
from app.dao.genre_dao import GenreDAO
from app.service.genre_service import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    genre1 = Genre(id=1, name='genre1')
    genre2 = Genre(id=2, name='genre2')
    genre3 = Genre(id=3, name='genre3')

    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    genre_dao.get_one = MagicMock(return_value=genre1)
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.update = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock(return_value=None)

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_all(self):
        all_genres = self.genre_service.get_all()

        assert len(all_genres) == 3, 'Неверное количество жанров'

    def test_get_one(self):
        one_genre = self.genre_service.get_one(1)

        assert one_genre.id == 1, 'Неверный жанр'
        assert one_genre.name == 'genre1', 'Неверный жанр'

    def test_create(self):
        data = {'name': 'genre4'}

        new_genre = self.genre_service.create(data)

        assert new_genre.id is not None, 'Неверный жанр'

    def test_update(self):
        data = {'name': 'genre4'}
        gid = 2

        self.genre_service.update(gid, data)

    def test_delete(self):
        self.genre_service.delete(1)
