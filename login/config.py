import os


class BaseConfig:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REPO_TYPE = 'MEM'

    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_TOKEN_ENDPOINT = os.environ.get('GOOGLE_TOKEN_ENDPOINT')
    GOOGLE_SCOPE = os.environ.get('GOOGLE_SCOPE')
    GOOGLE_AUTHORIZE_ENDPOINT = os.environ.get('GOOGLE_AUTHORIZE_ENDPOINT')

    KAKAO_REDIRECT_URI = os.environ.get('KAKAO_REDIRECT_URI')
    KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
    KAKAO_CLIENT_SECRET = os.environ.get('KAKAO_CLIENT_SECRET')
    KAKAO_TOKEN_ENDPOINT = os.environ.get('KAKAO_TOKEN_ENDPOINT')
    KAKAO_SCOPE = os.environ.get('KAKAO_SCOPE')
    KAKAO_AUTHORIZE_ENDPOINT = os.environ.get('KAKAO_AUTHORIZE_ENDPOINT')
    KAKAO_PROFILE_INFO_ENDPOINT = os.environ.get('KAKAO_PROFILE_INFO_ENDPOINT')

    OAUTH2_REFRESH_TOKEN_GENERATOR = True
    OAUTH2_TOKEN_EXPIRES_IN = {
        'authorization_code': 864000,
        'implicit': 3600,
        'password': 864000,
        'client_credentials': 864000
    }

    def init_app(self, app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REPO_TYPE = 'DB'

    def init_app(self, app):
        # app.debug = self.DEBUG
        pass


class ProductionConfig(BaseConfig):
    DEBUG = False
    REPO_TYPE = 'DB'

    def init_app(self, app):
        pass


config = {
    'dev': DevelopmentConfig,
    'prob': ProductionConfig
}
