from urllib.parse import urlencode

from flask import redirect, url_for, request
from flask_login import LoginManager

from login.proxy import user_repo

login_manager = LoginManager()


# 로그인된 사용자인지 판단하는 기능
@login_manager.user_loader
def load_user(user_id):
    return user_repo.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    # print(dir(request))
    # login이 필요한 page에 접근 시 login page로 이동을 시켜줌
    query_string = urlencode(request.args)

    return redirect(url_for('auth.login', next=f'{request.path}?{query_string}'))
