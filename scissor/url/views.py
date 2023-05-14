from ..utils import db
from flask_restx import Namespace, Resource

url_namespace= Namespace('url', description='Namespace for URLs')


@url_namespace.route('/')
class Url(Resource):
    def get(self):
        return {"message": "Hello World"}