import datetime as dt

import flask
from flask_restful import Resource
from sql.data.session import create_session
from sql.data.__all_models import *
from api.books.author_parser import parser

from api.errors import check_request


class AuthorsResource(Resource):
    def get(self, author_id):
        check_request(books.Author, author_id)
        session = create_session()
        author = session.query(books.Author).get(author_id)

        return flask.jsonify({"author": author.to_dict(only=("name", "birthday"))})

    def delete(self, author_id):
        check_request(books.Author, author_id)
        session = create_session()
        author = session.query(books.Author).get(author_id)
        session.delete(author)
        session.commit()

        return flask.jsonify({'success': 'OK'})


class AuthorsListResource(Resource):
    def get(self):
        session = create_session()
        all_authors = session.query(books.Author).all()
        return flask.jsonify({"authors": [item.to_dict(only=("name",
                                                             "birthday")) for item in all_authors]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        author = books.Author()
        author.name = args["name"]
        author.birthday = dt.datetime.strptime(args["birthday"], "%Y-%m-%d").date()

        session.add(author)
        session.commit()

        return flask.jsonify({"id": author.id})


class BooksAuthorsListResource(Resource):
    def get(self, book_id):
        check_request(books.Author, book_id)
        session = create_session()
        authors_books = session.query(books.Author).join(books.BooksAuthors).join(books.Book).filter(
            books.Book.id == book_id).all()

        return flask.jsonify({"books-authors": item.to_dict(only=("name", "birthday"))
                              for item in authors_books})
