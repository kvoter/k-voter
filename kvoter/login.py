from kvoter.db import User
from kvoter.app import app
from flask.ext.login import LoginManager


login_manager = LoginManager(app)

login_manager.login_view = 'login'


# TODO: Login view!


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)
