from authlib.integrations.flask_oauth2 import current_token
from flask import jsonify, Blueprint

from login.oauth.server import require_oauth

api = Blueprint('api', __name__)


@api.route("/me")
# profile 권한이 있는 token을 이용해야 접근이 가능하도록 설정
@require_oauth('profile')
def private_resource():
    user = current_token.user
    return jsonify(id=user.id, email=user.email)
