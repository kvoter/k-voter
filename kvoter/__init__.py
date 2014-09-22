from datetime import timedelta, datetime
from sqlalchemy.orm.exc import NoResultFound
from kvoter.app import app
from kvoter.db import User, db
from kvoter import login, routes


if __name__ == '__main__':
    db.create_all()

    try:
        User.query.filter(User.name == "admin").one()
    except NoResultFound:
        user = User("admin", "admin@kvoter.local", "admin", ["voter", "admin"])
        user.confirmed_at = datetime.now() - timedelta(days=2)
        db.session.add(user)
        db.session.commit()

    app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                "DO NOT COMMIT ME TO PRODUCTION")
    app.config["DEBUG"] = True
    app.run()
