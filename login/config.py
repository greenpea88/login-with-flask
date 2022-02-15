import os


class BaseConfig:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REPO_TYPE = 'MEM'

    def init_app(self, app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    def init_app(self, app):
        pass


class ProductionConfig(BaseConfig):
    DEBUG = False

    def init_app(self, app):
        pass


config = {
    'dev': DevelopmentConfig,
    'prob': ProductionConfig
}
