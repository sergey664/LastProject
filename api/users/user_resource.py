import flask
from flask_restful import Resource
from sql.data.session import create_session
from sql.data.__all_models import *

from api.errors import check_request


class UsersResource(Resource):
    def get(self, user_id):
        check_request(users.User, user_id)
        session = create_session()
        user = session.query(users.User).get(user_id)
        return flask.jsonify({"user": user.to_dict(only=("email", "nickname", "is_admin"))})


class UsersListResource(Resource):
    pass
