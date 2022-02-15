from flask import Flask, render_template

from login.auth import auth
from login.config import config
from login.database import db
from login.extentions import login_manager
from login.main import main


def create_app():
    app = Flask(__name__)
    app_config = config.get('dev')()
    app.config.from_object(app_config)
    app_config.init_app(app)

    init_extensions(app)
    init_db(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth, url_prefix="/auth")

    return app


def init_extensions(app):
    # flask-login 사용하기 >> app에 login manager 연결
    login_manager.init_app(app)


def init_db(app):
    db.init_app(app)
