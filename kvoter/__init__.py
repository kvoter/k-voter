from app import app
from db import db
import users

if __name__ == '__main__':
    db.create_all()

    users.get_or_create(user_name='admin',
                        password='admin',
                        email='admin@kvoter.local',
                        user_roles=['admin'])

    app.config["SECRET_KEY"] = ("I AM THE DEVELOPMENT SECRET KEY!"
                                "DO NOT COMMIT ME TO PRODUCTION")
    app.config["DEBUG"] = True
    app.run()
