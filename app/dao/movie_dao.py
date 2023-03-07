from sqlalchemy import desc

from app.dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, data):
        movies = self.session.query(Movie)

        if 'director_id' in data:
            movies = movies.filter(Movie.director_id == data['director_id'])

        if 'genre_id' in data:
            movies = movies.filter(Movie.genre_id == data['genre_id'])

        if 'year' in data:
            movies = movies.filter(Movie.year == data['year'])

        if 'status' in data and data['status'] == 'new':
            movies = movies.order_by(desc(Movie.id))

        if 'page' in data:
            movies_limit = 12
            movies_offset = (int(data['page']) - 1) * movies_limit
            movies = movies.limit(movies_limit).offset(movies_offset)

        if not data:
            movies = movies.all()

        return movies

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def create(self, data):
        new_movie = Movie(**data)

        self.session.add(new_movie)
        self.session.commit()

    def update(self, movie):
        self.session.add(movie)
        self.session.commit()

    def delete(self, mid):
        movie = self.get_one(mid)

        self.session.delete(movie)
        self.session.commit()
