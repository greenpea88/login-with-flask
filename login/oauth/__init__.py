from flask import Blueprint, request, render_template
from flask_login import current_user, login_required

from login.oauth.server import oauth_server

oauth = Blueprint('oauth', __name__)


@oauth.route('/authorize', methods=['GET', 'POST'])
@login_required
def authorize():
    # authorize code를 받아오는 부분 >> auth code를 받기 위해서는 login을 필요로 함
    # Login is required since we need to know the current resource owner.
    # It can be done with a redirection to the login page, or a login
    # form on this authorization page.
    if request.method == 'GET':
        # get으로 들어오는 경우 >> auth code 받기
        grant = oauth_server.get_consent_grant(end_user=current_user)
        client = grant.client
        scope = client.get_allowed_scope(grant.request.scope)
        # redirect uri는 필요하지 않은가?

        # You may add a function to extract scope into a list of scopes
        # with rich information, e.g.
        # scopes = describe_scope(scope)  # returns [{'key': 'email', 'icon': '...'}]
        return render_template(
            'authorize.html',
            grant=grant,
            user=current_user,
            client=client,
            scopes=scope,
        )
    # post로 들어오는 경우 >> implicit grants 부분???
    confirmed = request.form['confirm']
    if confirmed:
        # granted by resource owner
        # authorization이 성공한 경우
        return oauth_server.create_authorization_response(grant_user=current_user)
    # denied by resource owner
    # authorization 실패한 경우
    return oauth_server.create_authorization_response(grant_user=None)


@oauth.route('/token', methods=['POST'])
def issue_token():
    # 발급 받은 auth code를 이용해서 token 발급 받기
    return oauth_server.create_token_response()
