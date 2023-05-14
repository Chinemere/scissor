from flask import Flask
from .config.config import config_dict
from flask_restx import Api
from .utils import db
from .url.views import url_namespace

def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(url_namespace)
    return app