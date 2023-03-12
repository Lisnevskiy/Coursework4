from flask import Blueprint, request, abort

from app.implemented import user_service
from app.implemented import auth_service

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.post('/auth/register')
def create_user():
    reg_json = request.json

    try:
        new_user = user_service.create(reg_json)

        return '', 201, {"location": f"/users/{new_user.id}"}

    except:
        return {"message": "Error creating user"}, 400


@auth_bp.post('/auth/login')
def get_tokens():
    req_json = request.json

    email = req_json.get("email", None)
    password = req_json.get("password", None)

    if None in [email, password]:
        abort(400)

    tokens = auth_service.generate_tokens(email, password)

    return tokens, 201


@auth_bp.put('/auth/login')
def update_tokens():
    req_json = request.json

    token = req_json.get("refresh_token")

    tokens = auth_service.approve_refresh_token(token)

    return tokens, 201
