from db import db, user_datastore, User
import hashlib
from sqlalchemy.orm.exc import NoResultFound
import roles


def create_user(user_name,
                email,
                password,
                active=True,
                user_roles=['voters']):
    user_roles = [
        roles.get_or_create(role)
        for role in user_roles
    ]

    salt = hashlib.md5(bytes(user_name, 'utf8')).digest()

    password = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=bytes(password, 'utf8'),
        salt=salt,
        iterations=100000,
    )

    user_datastore.create_user(
        name=user_name,
        email=email,
        password=password,
        active=active,
        roles=user_roles,
    )
    db.session.commit()
    return User.query.filter(User.name == user_name).one()


def get_or_create(user_name,
                  email="",
                  password="",
                  active=True,
                  user_roles=['voters']):
    try:
        return User.query.filter(User.name == user_name).one()
    except NoResultFound:
        return create_user(
            user_name,
            email,
            password,
            active,
            user_roles,
        )
