from flask_restx import Resource, Namespace

from app.dao.model.genre import GenreSchema
from app.implemented import genre_service

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = genre_service.get_all()

        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre = genre_service.get_one(gid)

        if not genre:
            return {'message': 'Genre not found'}, 404

        return genre_schema.dump(genre), 200
