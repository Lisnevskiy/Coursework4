from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.genre import GenreSchema
from app.implemented import genre_service

from app.helpers.decorators import auth_required, admin_required


genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenreView(Resource):
    @auth_required
    def get(self):
        genres = genre_service.get_all()

        return genres_schema.dump(genres), 200

    @admin_required
    def post(self):
        reg_json = request.json

        genre_service.create(reg_json)

        return '', 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_one(gid)

        if not genre:
            return {'message': 'Genre not found'}, 404

        return genre_schema.dump(genre), 200

    @admin_required
    def put(self, gid):
        reg_json = request.json

        try:
            genre_service.update(gid, reg_json)

            return '', 204

        except:
            return {'message': 'Genre not found, or another error'}, 404

    @admin_required
    def delete(self, gid):
        try:
            genre_service.delete(gid)

            return '', 204

        except:
            return {'message': 'Genre not found, or another error'}, 404
