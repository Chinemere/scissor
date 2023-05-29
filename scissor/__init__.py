from flask import Flask
from .config.config import config_dict
from flask_restx import Api
from .utils import db
from .url.views import url_namespace
from .auth.views import auth_namespace
from .models.users import User
from .models.url import Url
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .users.views import user_namespace
# from flask_caching import Cache
from .utils import caches



def create_app(config=config_dict['dev']):
    global app
    app=Flask(__name__)
    app.config.from_object(config)

    app.config['CACHE_TYPE'] = 'simple'

    caches.init_app(app)

    api = Api(app)

    
    api.add_namespace(url_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(user_namespace, path='/users')
    from .frontend_views import home_namespace
    api.add_namespace(home_namespace, path='/home')

    
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt= JWTManager(app)
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User':User,
            'Url': Url
        }
    return app
