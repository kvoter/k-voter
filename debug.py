#! /usr/bin/env python
from datetime import timedelta, datetime
import kvoter
from kvoter.db import db, User
from sqlalchemy.orm.exc import NoResultFound

if __name__ == '__main__':
    db.create_all()

    try:
        User.query.filter(User.name == "admin").one()
    except NoResultFound:
        user = User("admin", "admin@kvoter.local", "admin", ["voter", "admin"])
        user.confirmed_at = datetime.now() - timedelta(days=2)
        db.session.add(user)
        db.session.commit()

    kvoter.app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                       "DO NOT COMMIT ME TO PRODUCTION")
    kvoter.app.config["DEBUG"] = True
    kvoter.app.run()
