from app import app
from db import db
import users

if __name__ == '__main__':
    db.create_all()

    users.get_or_create(name='admin',
                        password='admin',
                        email='admin@kvoter.local')

    app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                "DO NOT COMMIT ME TO PRODUCTION")
    app.config["DEBUG"] = True
    app.run()
