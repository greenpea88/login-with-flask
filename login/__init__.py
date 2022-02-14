from flask import Flask, render_template

from login.auth import auth
from login.extentions import login_manager
from login.main import main
from login.models import user_pool, User


def create_app():
    app = Flask(__name__)
    
    app.secret_key = 'secret'

    init_extensions(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth, url_prefix="/auth")

    return app


def init_extensions(app):
    # flask-login 사용하기 >> app에 login manager 연결
    login_manager.init_app(app)

    # 로그인된 사용자인지 판단하는 기능
    @login_manager.user_loader
    def load_user(user_id):
        target_user = None
        for user in user_pool:
            if user.get('id') == user_id:
                target_user = user

        if target_user:
            return User(target_user.get('id'), target_user.get('email'), target_user.get('name'), target_user.get('password'))

