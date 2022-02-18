from sqlalchemy.orm import relationship

from login.database import db

from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin, OAuth2AuthorizationCodeMixin

from login.domain.user import UserEntity


class User(db.Model):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", Unicode, nullable=False)

    def to_entity(self):
        return UserEntity(self.id, self.email, self.name, self.password)


class Connection(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)

    # user entity와 relation
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User', backref="connections")

    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))


# [client] - client_id, client_secret, client_metadata, expires_at
class Client(db.Model, OAuth2ClientMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete='CASCADE')
    )
    user = relationship('User')


# [token] - access_token, refresh_token, expires_at, scope, client_id
# 발급 받은 token에 대한 정보 저장
class Token(db.Model, OAuth2TokenMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete='CASCADE')
    )
    user = db.relationship('User')


# [auth code] - code, redirect_uri, response_type, scope, client_id, nonce, auth_time
# 발급 받은 auth code에 대한 정보 저장
class AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete='CASCADE')
    )
    user = db.relationship('User')
