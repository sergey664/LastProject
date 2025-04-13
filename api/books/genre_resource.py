import flask
from flask_restful import Resource
from sql.data.session import create_session
from sql.data.__all_models import *
from api.books.genre_parser import parser

from api.errors import check_request


class GenresResource(Resource):
    def get(self, genre_id):
        check_request(books.Genre, genre_id)
        session = create_session()
        genre = session.query(books.Genre).get(genre_id)

        return flask.jsonify({"genre": genre.to_dict(only=("name", ))})

    def delete(self, genre_id):
        check_request(books.Genre, genre_id)
        session = create_session()
        genre = session.query(books.Author).get(genre_id)
        session.delete(genre)
        session.commit()

        return flask.jsonify({'success': 'OK'})


class GenresListResource(Resource):
    def get(self):
        session = create_session()
        all_genres = session.query(books.Genre).all()
        return flask.jsonify({"genres": [item.to_dict(only=("name", )) for item in all_genres]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        genre = books.Genre()
        genre.name = args["name"]

        session.add(genre)
        session.commit()

        return flask.jsonify({"id": genre.id})
