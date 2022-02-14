from werkzeug.local import LocalProxy

from login.repositories.user import DBUserRepo


def get_user_repo():
    global _repo

    if not _repo:
        _repo = DBUserRepo()

    return _repo


user_repo = LocalProxy(get_user_repo())
