from authlib.oauth2 import OAuth2Error
from flask import Blueprint, request, render_template, current_app
from flask_login import current_user, login_required

from login.oauth.server import oauth_server

oauth = Blueprint('oauth', __name__)


# authorize code를 받아오는 부분 >> auth code를 받기 위해서는 login을 필요로 함
@oauth.route('/authorize', methods=['GET', 'POST'])
@login_required
def authorize():
    # Login is required since we need to know the current resource owner.
    # It can be done with a redirection to the login page, or a login
    # form on this authorization page.
    if request.method == 'GET':
        # get으로 들어오는 경우 >> 사용자로부터 consent 받기
        # 사용자에게 consent를 받는 부분
        try:
            # grant = oauth_server.get_consent_grant(end_user=current_user)
            grant = oauth_server.validate_consent_request(end_user=current_user)
            client = grant.client
            scope = client.get_allowed_scope(grant.request.scope)
        except OAuth2Error as error:
            current_app.logger.exception('oauth-error')
            return error.error

        # You may add a function to extract scope into a list of scopes
        # with rich information, e.g.
        # scopes = describe_scope(scope)  # returns [{'key': 'email', 'icon': '...'}]
        return render_template(
            'oauth/authorize.html',
            grant=grant,
            user=current_user,
            client=client,
            scopes=scope,
        )

    # post로 들어오는 경우 >> 사용자의 동의 여부를 전송
    # form에 동의하시겠습니까? -> 동의했는지의 여부를 서버로 보내줘야하기 때문에
    # client setting >> consent를 받는지 여부에 따라서 달라지는 부분
    # option : skip_content = true 이런 식으로
    confirmed = request.form['confirm']
    if confirmed:
        # granted by resource owner
        # 동의를 한 경우
        return oauth_server.create_authorization_response(grant_user=current_user)
    # denied by resource owner
    # 동의를 하지 않은 경우
    return oauth_server.create_authorization_response(grant_user=None)


# token 발급
@oauth.route('/token', methods=['POST'])
def issue_token():
    return oauth_server.create_token_response()
