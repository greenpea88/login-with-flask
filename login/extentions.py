from flask_login import LoginManager

from login.proxy import user_repo

login_manager = LoginManager()


# 로그인된 사용자인지 판단하는 기능
@login_manager.user_loader
def load_user(user_id):
    return user_repo.get(user_id)
