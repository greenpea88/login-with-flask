from login.database import db
from login.models import UserEntity, User
from login.repositories import BaseUserRepo


class MemUserRepo(BaseUserRepo):

    def __init__(self, init_data):
        self.data = init_data

    def get(self, user_id):
        target_user = None
        for user in self.data:
            if user.get('id') == user_id:
                target_user = user

        if target_user:
            return UserEntity(
                target_user.get('id'),
                target_user.get('email'),
                target_user.get('name'),
                target_user.get('password')
            )

    def get_by_email(self, email, password):
        target_user = None

        for user in self.data:
            if user.get('email') == email and user.get('password') == password:
                target_user = user

        if target_user:
            return UserEntity(
                target_user.get('id'),
                target_user.get('email'),
                target_user.get('name'),
                target_user.get('password')
            )

    def list(self):
        pass


class DBUserRepo(BaseUserRepo):
    def get(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            return UserEntity(
                user.id,
                user.email,
                user.name,
                user.password
            )

    def get_by_email(self, email, password):
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            return UserEntity(
                user.id,
                user.email,
                user.name,
                user.password
            )

    def list(self):
        pass
