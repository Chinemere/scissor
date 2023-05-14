import os
from decouple import config

BASE_DIR= os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URL='sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True


class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass


config_dict={
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}