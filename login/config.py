import os


class BaseConfig:
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # REPO_TYPE = 'MEM'

    GOOGLE_REDIRECT_URI = "http://localhost:5000/auth/oauth/callback/google"
    GOOGLE_CLIENT_ID = "670786064026-t3jg68nvsno4fjh88nsfe0nqu4d1k14k.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "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"
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    GOOGLE_SCOPE = "openid profile"
    GOOGLE_AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/auth"

    # KAKAO_REDIRECT_URI = "http://localhost:5000/auth/oauth/callback/kakao"
    # KAKAO_CLIENT_ID =
    # KAKAO_CLIENT_SECRET =
    # KAKAO_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
    # KAKAO_SCOPE =
    # KAKAO_AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"

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

    def init_app(self, app):
        pass


config = {
    'dev': DevelopmentConfig,
    'prob': ProductionConfig
}
