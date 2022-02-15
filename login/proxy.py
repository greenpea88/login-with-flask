from flask import current_app
from werkzeug.local import LocalProxy

from login.repositories.user import DBUserRepo, MemUserRepo

_repo = None


def get_user_repo():
    global _repo

    if not _repo:
        # current_app <-- flask app context
        if current_app.config.get('REPO_TYPE', 'DB') == 'DB':
            _repo = DBUserRepo()
        else:
            _repo = MemUserRepo([
                {
                    'id': 1,
                    'email': 'test@test.com',
                    'name': '테스트',
                    'password': 'secret'
                },
            ])

    return _repo


user_repo = LocalProxy(get_user_repo)
