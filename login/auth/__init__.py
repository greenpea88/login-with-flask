import jwt
from urllib.parse import urlencode

import requests
from flask import Blueprint, request, render_template, url_for, redirect, current_app, abort, flash
from flask_login import login_user, logout_user

from login.auth.form import RegisterForm
from login.models import User, Connection
from login.database import db
from login.proxy import user_repo

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # 회원가입
    form = RegisterForm()

    if request.method == 'POST':
        # username = request.form.get('username')
        # email = request.form.get('email')
        # password = request.form.get('password')
        # password_confirm = request.form.get('password_confirm')

        if form.validate_on_submit():
            username = form.data.get('username')
            email = form.data.get('email')
            password = form.data.get('password')


            user = User()
            user.email = email
            user.name = username
            user.password = password

            db.session.add(user)
            db.session.commit()

            flash('회원 가입이 완료되었습니다.')
            return redirect(url_for('index'))
        else:
            flash('입력한 값을 확인해주세요.')

    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        next = request.args.get('next', '') # login 후 이동할 페이지 지정

    else:
        # form 방식으로 받아올 때에는 form에, json 방식으로 받아올 때에는 json에 원하는 정보가 담겨있음
        email = request.form.get('email')
        password = request.form.get('password')
        next = request.form.get('next')
        safe_next_redirect = url_for('index')

        if next:
            safe_next_redirect = next

        user = user_repo.get_by_email(email)
        if user.password == password:
            login_user(user)
            return redirect(safe_next_redirect)

    return render_template('auth/login.html', next=next)


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

    user_data = jwt.decode(resp.json()['id_token'], options={"verify_signature": False})

    name = user_data['name']
    email = user_data['email']
    user = db.session.query(User).filter(User.email == email).first()

    if not user:
        # 존재하지 않는 user인 경우 회원가입 시켜주기
        user = User(
            name=name,
            email=email,
            password=""
        )
        db.session.add(user)
        db.session.commit()

    login_user(user.to_entity())

    connection = Connection()
    connection.provider_id = "google"
    connection.user = user
    connection.access_token = resp.json().get('access_token')
    db.session.commit()

    return redirect(url_for("index"))


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

    access_token = resp.json().get('access_token')
    profile_info_endpoint = current_app.config.get('KAKAO_PROFILE_INFO_ENDPOINT')
    profile_resp = requests.get(profile_info_endpoint,
                                headers=dict(authorization=f'Bearer {access_token}'))
    user_data = profile_resp.json()['kakao_account']

    name = user_data['profile']['nickname']
    email = user_data['email']
    user = db.session.query(User).filter(User.email == email).first()

    if not user:
        # 존재하지 않는 user인 경우 회원가입 시켜주기
        user = User(
            name=name,
            email=email,
            password=""
        )
        db.session.add(user)
        db.session.commit()

    login_user(user.to_entity())

    connection = Connection()
    connection.provider_id = "kakao"
    connection.user = user
    connection.access_token = access_token
    db.session.commit()

    return redirect(url_for("index"))


@auth.route('/logout', methods=['GET'])
def logout():
    # flask login으로 logout >> 사용자 정보 세션 삭제
    logout_user()
    return redirect(url_for('index'))

