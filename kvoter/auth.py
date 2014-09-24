from kvoter.db import User
from kvoter.app import app
from flask.ext.login import LoginManager, login_user, logout_user
from flask import request, render_template, redirect, url_for
from wtforms import Form, TextField, PasswordField, validators
from sqlalchemy.orm.exc import NoResultFound


login_manager = LoginManager(app)

login_manager.login_view = 'login'


class LoginForm(Form):
    username = TextField(
        'Username',
        [
            validators.Length(min=3, max=30),
            validators.Required()
        ],
    )
    password = PasswordField(
        'Password',
        [
            validators.Required(),
        ],
    )


def login_view():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        try:
            user = User.query.filter(User.name == form.username.data).one()
        except NoResultFound:
            # The user does not exist
            user = None
        if user and user.validate_password(form.password.data):
            # The user exists and the password is valid
            login_user(user)
            # TODO: We need to make sure that 'next' points to something on our
            # site to avoid malicious redirects
            return redirect(request.args.get('next') or url_for('home_page'))
        else:
            # TODO: Return "Username or password was incorrect, forgot link
            return 'Whoops'
    else:
        return render_template("login.html", form=form)


def logout_view():
    logout_user()
    return redirect(url_for('home_page'))


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)
