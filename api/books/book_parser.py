from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument("title", required=True)
parser.add_argument("year", required=True)
parser.add_argument("description", required=True)
parser.add_argument("file", required=True)
parser.add_argument("authors", required=True)
parser.add_argument("genres", required=True)
