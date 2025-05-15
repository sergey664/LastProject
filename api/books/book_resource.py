import flask
from flask_restful import Resource
from sql.data.session import create_session
from sql.data.__all_models import *
from api.books.book_parser import parser

from api.errors import check_request


class BooksResource(Resource):
    def get(self, book_id):
        check_request(books.Book, book_id)
        session = create_session()
        book = session.query(books.Book).get(book_id)

        return flask.jsonify({"book": book.to_dict(only=("id", "title", "year", "description", "file"))})

    @staticmethod
    def delete(book_id):
        check_request(books.Book, book_id)
        session = create_session()
        book = session.query(books.Book).get(book_id)
        session.delete(book)
        session.commit()

        return flask.jsonify({'success': book.file})


class BooksListResource(Resource):
    def get(self):
        session = create_session()
        all_books = session.query(books.Book).all()
        return flask.jsonify({"books": [item.to_dict(only=("id", "title", "year", "description", "file"))
                                        for item in all_books]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        book = books.Book()
        book.title = args["title"]
        book.year = args["year"]
        book.description = args["description"]
        book.file = args["file"]

        session.add(book)

        book.authors = session.query(books.Author).filter(books.Author.id.in_([*args["authors"]])).all()
        book.genres = session.query(books.Genre).filter(books.Genre.id.in_([*args["genres"]])).all()

        session.commit()

        return flask.jsonify({"id": book.id})


class AuthorsBooksListResource(Resource):
    def get(self, author_id):
        check_request(books.Author, author_id)
        session = create_session()
        authors_books = session.query(books.Book).join(books.BooksAuthors).join(books.Author).filter(books.Author.id == author_id).all()

        return flask.jsonify({"authors-books": [item.to_dict(only=("id", "title", "year", "description", "file"))
                              for item in authors_books]})


class GenreBooksListResource(Resource):
    def get(self, genre_id):
        check_request(books.Genre, genre_id)
        session = create_session()
        genre_books = session.query(books.Book).join(books.BooksGenres).join(books.Genre).filter(books.Genre.id == genre_id).all()

        return flask.jsonify({"genre-books": [item.to_dict(only=("id", "title", "year", "description", "file"))
                              for item in genre_books]})
