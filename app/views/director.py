from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.director import DirectorSchema
from app.implemented import director_service

from app.helpers.decorators import auth_required, admin_required


directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorView(Resource):
    @auth_required
    def get(self):
        directors = director_service.get_all()

        return directors_schema.dump(directors), 200

    @admin_required
    def post(self):
        reg_json = request.json

        director_service.create(reg_json)

        return '', 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        director = director_service.get_one(did)

        if not director:
            return {'message': 'Director not found'}, 404

        return director_schema.dump(director), 200

    @admin_required
    def put(self, did):
        reg_json = request.json

        try:
            director_service.update(did, reg_json)

            return '', 204

        except:
            return {'message': 'Director not found, or another error'}, 404

    @admin_required
    def delete(self, did):
        try:
            director_service.delete(did)

            return '', 204

        except:
            return {'message': 'Director not found, or another error'}, 404
