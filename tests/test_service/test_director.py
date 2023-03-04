from unittest.mock import MagicMock

import pytest

from app.dao.model.director import Director
from app.dao.director_dao import DirectorDAO
from app.service.director_service import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    director1 = Director(id=1, name='director1')
    director2 = Director(id=2, name='director2')
    director3 = Director(id=3, name='director3')

    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.update = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock(return_value=None)

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_all(self):
        all_directors = self.director_service.get_all()

        assert len(all_directors) == 3, 'Неверное количество режиссеров'

    def test_get_one(self):
        one_director = self.director_service.get_one(1)

        assert one_director.id == 1, 'Неверный режиссер'
        assert one_director.name == 'director1', 'Неверный режиссер'

    def test_create(self):
        data = {'name': 'director4'}

        new_director = self.director_service.create(data)

        assert new_director.id is not None, 'Неверный режиссер'

    def test_update(self):
        data = {'name': 'director4'}
        did = 2

        self.director_service.update(did, data)

    def test_delete(self):
        self.director_service.delete(1)
