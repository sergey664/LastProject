from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)
parser.add_argument("is_admin", required=True)
parser.add_argument("nickname", required=True)
