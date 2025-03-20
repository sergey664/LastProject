import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Book(SqlAlchemyBase):
    pass


class Genre(SqlAlchemyBase):
    pass


class Author(SqlAlchemyBase):
    pass
