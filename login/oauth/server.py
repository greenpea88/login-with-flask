from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.integrations.sqla_oauth2 import create_bearer_token_validator

from login.oauth.grants import AuthorizationCodeGrant, PasswordGrant, RefreshTokenGrant
from login.database import db
from login.models import Client, Token



def query_client(client_id):
    return db.session.query(Client).filter_by(client_id=client_id).first()


def save_token(token_data, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        # user_id = None

    token = Token(
        client_id=request.client.client_id,
        user_id=user_id,
        **token_data
    )
    db.session.add(token)
    db.session.commit()


oauth_server = AuthorizationServer()
require_oauth = ResourceProtector()
