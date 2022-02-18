from sqlalchemy.orm import relationship

from login.database import db

from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin, OAuth2TokenMixin


class UserEntity:
    def __init__(self, id, email, name, password):
        self.id = id
        self.email = email
        self.name = name
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"USER: {self.id} = {self.name}"


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


class Client(db.Model, OAuth2ClientMixin):
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(User.id, ondelete='CASCADE')
    )
    user = relationship('User')


class Token(db.Model, OAuth2TokenMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey(User.id, ondelete='CASCADE')
    )
    user = db.relationship('User')
