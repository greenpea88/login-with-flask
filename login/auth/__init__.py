from flask import Blueprint, request, render_template, url_for, redirect
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


@auth.route('/logout', methods=['GET'])
def logout():
    # flask login으로 logout >> 사용자 정보 세션 삭제
    logout_user()
    return redirect(url_for('index'))

