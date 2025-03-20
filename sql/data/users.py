import sqlalchemy as sa
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class UserType(SqlAlchemyBase):
    __tablename__ = 'user_types'

    type_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    type_name = sa.Column(sa.String)


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    user_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_name = sa.Column(sa.String, unique=True)
    user_email = sa.Column(sa.String, unique=True)
    user_password = sa.Column(sa.String, unique=True)

    user_type = sa.Column(sa.Integer, sa.ForeignKey("user_types.type_id"))
    users = orm.relationship('UserType')
