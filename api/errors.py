import flask
from sql.data.session import create_session


def check_request(request_type, request):
    session = create_session()
    result = session.query(request_type).get(request)
    if not result:
        flask.abort(404, message="Request Not Found...")
