from flask import Blueprint
from flask_login import login_required

oauth = Blueprint('oauth', __name__)

# @oauth.route('/authorize', methods=['GET', 'POST'])
# @login_required
# def authorize():
#