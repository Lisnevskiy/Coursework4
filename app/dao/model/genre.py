from marshmallow import Schema, fields
from app.setup_db import db


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()
