from flask import request
from flask_restx import Resource, Namespace

from app.dao.model.user import UserSchema
from app.helpers.decorators import admin_required
from app.implemented import user_service

users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/')
class UsersView(Resource):
    def get(self):
        all_users = user_service.get_all()

        return users_schema.dump(all_users), 200


@users_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)

        if not user:
            return {"message": "User not found"}, 404

        return user_schema.dump(user), 200

    def patch(self, uid):
        reg_json = request.json

        try:
            user_service.update_partial(uid, reg_json)

            return '', 204

        except:
            return {'message': 'User not found, or another error'}, 404

    def put(self, uid):
        reg_json = request.json

        try:
            user_service.update_partial(uid, reg_json)

            return '', 204

        except:
            return {'message': 'User not found, or another error'}, 404

    @admin_required
    def delete(self, uid):
        try:
            user_service.delete(uid)

            return '', 204

        except:
            return {'message': 'User not found, or another error'}, 404


@users_ns.route('/<int:uid>/password')
class UserPasswordView(Resource):
    def put(self, uid):
        reg_json = request.json

        user_service.update_password(uid, reg_json)

        return '', 204
