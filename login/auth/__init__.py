import requests
from urllib.parse import urlencode

from flask import Blueprint, request, render_template, url_for, redirect, current_app, abort
from flask_login import login_user, logout_user

from login.proxy import user_repo

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    next = request.form.get('next', '')  # login 후 이동할 페이지 지정
    print(next)

    if request.method == 'GET':
        return render_template('auth/login.html')

    else:
        # form 방식으로 받아올 때에는 form에, json 방식으로 받아올 때에는 json에 원하는 정보가 담겨있음
        email = request.form.get('email')
        password = request.form.get('password')
        safe_next_redirect = url_for('index')

        if next:
            safe_next_redirect = next

        user = user_repo.get_by_email(email, password)
        if not user:
            return render_template('auth/login.html', error='grant failed')

        login_user(user)

    return redirect(safe_next_redirect)


@auth.route('/login/authorize/<target>', methods=['GET'])
def authorize(target):
    # authorization code 받아오기
    if target not in ['google', 'kakao']:
        # error 발생시키기
        return abort(404)

    target = str.upper(target)

    authorize_endpoint = current_app.config.get(f'{target}_AUTHORIZE_ENDPOINT')
    client_id = current_app.config.get(f'{target}_CLIENT_ID')
    redirect_uri = current_app.config.get(f'{target}_REDIRECT_URI')
    response_type = "code"
    scope = current_app.config.get(f'{target}_SCOPE')

    query_string = urlencode(dict(
        redirect_uri=redirect_uri,
        client_id=client_id,
        scope=scope,
        response_type=response_type
    ))

    authorize_redirect = f'{authorize_endpoint}?{query_string}'

    return redirect(authorize_redirect)


@auth.route('/oauth/callback/google', methods=['GET'])
def google_callback():
    code = request.args.get('code')
    token_endpoint = current_app.config.get('GOOGLE_TOKEN_ENDPOINT')
    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = current_app.config.get('GOOGLE_REDIRECT_URI')
    grant_type = 'authorization_code'

    resp = requests.post(token_endpoint, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type
    ))

    # return code
    return resp.json()
    # return redirect("/")


@auth.route('/oauth/callback/kakao', methods=['GET'])
def kakao_callback():
    code = request.args.get('code')
    token_endpoint = current_app.config.get('KAKAO_TOKEN_ENDPOINT')
    client_id = current_app.config.get('KAKAO_CLIENT_ID')
    client_secret = current_app.config.get('KAKAO_CLIENT_SECRET')
    redirect_uri = current_app.config.get('KAKAO_REDIRECT_URI')
    grant_type = 'authorization_code'

    resp = requests.post(token_endpoint, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type
    ))

    # return code
    return resp.json()


@auth.route('/logout', methods=['GET'])
def logout():
    # flask login으로 logout >> 사용자 정보 세션 삭제
    logout_user()
    return redirect(url_for('index'))

