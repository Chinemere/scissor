from flask import Flask
from .config.config import config_dict
from flask_restx import Api
from .utils import db
from .url.views import url_namespace
from .auth.views import auth_namespace
from .models.users import User
from .models.url import Url
from flask_migrate import Migrate


def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)

    api = Api(app)

    api.add_namespace(url_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    db.init_app(app)
    migrate = Migrate(app, db)
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User':User,
            'Url': Url
        }
    return app