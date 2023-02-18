from flask_restx import Resource, Namespace

from app.dao.model.director import DirectorSchema
from app.implemented import director_service

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = director_service.get_all()

        return directors_schema.dump(directors), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = director_service.get_one(did)

        if not director:
            return {'message': 'Director not found'}, 404

        return director_schema.dump(director), 200
