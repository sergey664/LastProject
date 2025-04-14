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

        return flask.jsonify({"book": book.to_dict(only=("title", "birthday", "description", "file"))})

    def delete(self, book_id):
        check_request(books.Book, book_id)
        session = create_session()
        book = session.query(users.User).get(book_id)
        session.delete(book)
        session.commit()

        return flask.jsonify({'success': 'OK'})


class BooksListResource(Resource):
    def get(self):
        session = create_session()
        all_books = session.query(books.Book).all()
        return flask.jsonify({"books": [item.to_dict(only=("title", "birthday", "description", "file"))
                                        for item in all_books]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        book = books.Book()
        book.title = args["title"]
        book.nickname = args["birthday"]
        book.description = args["description"]
        book.file = args["file"]

        session.add(book)
        session.commit()

        return flask.jsonify({"id": book.id})


class AuthorsBooksListResource(Resource):
    def get(self, author_id):
        check_request(books.Author, author_id)
        session = create_session()
        authors_books = session.query(books.Book).join(books.BooksAuthors).join(books.Author).filter(books.Author.id == author_id).all()

        return flask.jsonify({"authors-books": item.to_dict(only=("title", "birthday", "description", "file"))
                              for item in authors_books})
