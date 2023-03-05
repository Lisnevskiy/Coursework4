from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.movie import MovieSchema
from app.implemented import movie_service

from app.helpers.decorators import auth_required, admin_required

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MovieView(Resource):
    @auth_required
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        page = request.args.get('page', type=int)

        if genre_id:
            movies = movie_service.get_by_genre_id(genre_id)

            if not movies:
                return {'message': 'No movies found'}, 404

            return movies_schema.dump(movies), 200

        if director_id:
            movies = movie_service.get_by_director_id(director_id)

            if not movies:
                return {'message': 'No movies found'}, 404

            return movies_schema.dump(movies), 200

        if year:
            movies = movie_service.get_by_year(year)

            if not movies:
                return {'message': 'No movies found'}, 404

            return movies_schema.dump(movies), 200

        if page:
            movies = movie_service.get_by_page(page)

            if not movies:
                return {'message': 'No movies found'}, 404

            return movies_schema.dump(movies), 200

        movies = movie_service.get_all()

        return movies_schema.dump(movies), 200

    @admin_required
    def post(self):
        reg_json = request.json

        movie_service.create(reg_json)

        return '', 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):

    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)

        if not movie:
            return {'message': 'Movie not found'}, 404

        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid):
        reg_json = request.json

        try:
            movie_service.update_partial(mid, reg_json)

            return '', 204

        except:
            return {'message': 'Movie not found, or another error'}, 404

    @admin_required
    def delete(self, mid):
        try:
            movie_service.delete(mid)

            return '', 204

        except:
            return {'message': 'Movie not found, or another error'}, 404
