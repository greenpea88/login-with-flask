from flask import Flask, render_template

from login.auth import auth
from login.extentions import login_manager
from login.main import main


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'

    # init_extensions(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth, url_prefix="/auth")

    return app


def init_extensions(app):
    # flask-login 사용하기
    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     target_user = None

