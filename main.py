from flask import Flask
from flask_restx import Api

from app.config import Config
from app.setup_db import db

from app.views.errorhandler import errorhandler_bp

from app.views.director import directors_ns
from app.views.genre import genres_ns
from app.views.movie import movies_ns
from app.views.user import users_ns
from app.views.auth import auth_ns


def create_app(config_object):
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()

    return application


def configure_app(application):
    db.init_app(application)
    api = Api(application)

    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)

    application.register_blueprint(errorhandler_bp)


app = create_app(Config())
configure_app(app)


if __name__ == '__main__':
    app.run(debug=True)
