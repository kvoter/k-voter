from app import app
from db import db, user_datastore

if __name__ == '__main__':
    @app.before_first_request
    def create_user():
        db.create_all()
        user_datastore.create_user(email='admin@kvoter.org.uk',
                                   password='admin')
        db.session.commit()

    app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                "DO NOT COMMIT ME TO PRODUCTION")
    app.config["DEBUG"] = True
    app.run()
