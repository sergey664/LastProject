import sqlalchemy
from .session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


BooksAuthors = sqlalchemy.Table(
    "books_authors",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column("authors", sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id"))
)


BooksGenres = sqlalchemy.Table(
    "books_genres",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column("genres", sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
)


class Author(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "authors"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    birthday = sqlalchemy.Column(sqlalchemy.Date)

    books = sqlalchemy.orm.relationship("Book", secondary="books_authors", back_populates="authors")


class Genre(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "genres"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    books = sqlalchemy.orm.relationship("Book", secondary="books_genres", back_populates="genres")


class Book(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String, unique=True)
    file = sqlalchemy.Column(sqlalchemy.String)

    genres = sqlalchemy.orm.relationship("Genre", secondary="books_genres", back_populates="books")
    authors = sqlalchemy.orm.relationship("Author", secondary="books_authors", back_populates="books")
