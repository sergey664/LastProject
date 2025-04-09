import flask
from flask_restful import Resource
from sql.data.session import create_session
from sql.data.__all_models import *
from api.users.user_parser import parser

from api.errors import check_request


class UsersResource(Resource):
    def get(self, user_id):
        check_request(users.User, user_id)
        session = create_session()
        user = session.query(users.User).get(user_id)

        return flask.jsonify({"user": user.to_dict(only=("email", "nickname", "is_admin"))})

    def delete(self, user_id):
        check_request(users.User, user_id)
        session = create_session()
        user = session.query(users.User).get(user_id)
        session.delete(user)
        session.commit()

        return flask.jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = create_session()
        all_users = session.query(users.User).all()
        return flask.jsonify({"users": [item.to_dict(only=("email", "nickname", "is_admin")) for item in all_users]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        user = users.User()
        user.email = args["email"]
        user.nickname = args["nickname"]
        user.set_password(args["password"])

        session.add(user)
        session.commit()

        return flask.jsonify({"id": user.id})
