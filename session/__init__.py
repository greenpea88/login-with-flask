from flask import Flask, render_template

from session.auth import auth
from session.main import main


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
