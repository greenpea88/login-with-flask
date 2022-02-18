from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from login.auth import auth
from login.config import config
from login.database import db, migrate
from login.extentions import login_manager
from login.main import main
from login.models import User, Connection, Client, Token, AuthorizationCode
from login.oauth import oauth
from login.oauth.server import oauth_server, query_client, save_token


def create_app():
    app = Flask(__name__)
    app_config = config.get('dev')()
    # flask의 설정값 사용 --> 1. .py file 2. 환경 변수 3. config object(class)를 이용해 설정 가능
    app.config.from_object(app_config)
    app_config.init_app(app)

    init_extensions(app)
    init_db(app)
    init_oauth(app)

    if app.debug:
        # debug mode 일 때만 admin page를 만들도록
        init_admin(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(oauth, url_prefix="/oauth")

    return app


def init_extensions(app):
    # flask-login 사용하기 >> app에 login manager 연결
    login_manager.init_app(app)


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def init_oauth(app):
    oauth_server.init_app(app, query_client=query_client, save_token=save_token)


def init_admin(app):
    admin = Admin(app, name='flask login', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Connection, db.session))
    admin.add_view(ModelView(Client, db.session))
    admin.add_view(ModelView(Token, db.session))
    admin.add_view(ModelView(AuthorizationCode, db.session))
