from app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import (RoleMixin, Security, SQLAlchemyUserDatastore,
                                UserMixin)
import hashlib

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kvoter.db"

db = SQLAlchemy(app)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        salt = hashlib.md5(bytes(self.name, 'utf8')).digest()
        self._password = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=bytes(value, 'utf8'),
            salt=salt,
            iterations=100000,
        )


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
