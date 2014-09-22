from db import db, user_datastore, Role
from sqlalchemy.orm.exc import NoResultFound


def create_role(name, description=""):
    user_datastore.create_role(
        name=name,
        description=description,
    )
    db.session.commit()
    return Role.query.filter(Role.name == name).one()


def get_or_create(name, description=""):
    try:
        return Role.query.filter(Role.name == name).one()
    except NoResultFound:
        return create_role(name, description)
