from datetime import timedelta, datetime
from flask import render_template
from flask.ext.login import login_required
from sqlalchemy.orm.exc import NoResultFound
from kvoter.app import app
from kvoter.db import User, db
from kvoter import login


@app.route("/")
def home_page():  # Why does this throw an exception?
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")


if __name__ == '__main__':
    db.create_all()

    @app.before_first_request
    def get_or_create_debug_admin_user():
        try:
            return User.query.filter(User.name == "admin").one()
        except NoResultFound:
            user = User("admin", "admin@kvoter.local", "admin", ["voter", "admin"])
            user.confirmed_at = datetime.now() - timedelta(days=2)
            db.session.commit()

    app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                "DO NOT COMMIT ME TO PRODUCTION")
    app.config["DEBUG"] = True
    app.run()
