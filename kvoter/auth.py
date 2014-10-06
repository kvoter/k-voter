from kvoter.db import User, Election, Candidate, Voter
from kvoter.app import app
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)
from flask import request, render_template, redirect, url_for, flash
from wtforms import Form, TextField, PasswordField, validators, IntegerField
from sqlalchemy.orm.exc import NoResultFound


login_manager = LoginManager(app)
login_manager.login_view = 'login'


class LoginForm(Form):
    username = TextField(
        'Username',
        [
            validators.Length(max=64),
            validators.Required()
        ],
    )
    password = PasswordField(
        'Password',
        [
            validators.Required(),
        ],
    )


class RegisterForm(Form):
    username = TextField(
        'Username',
        [
            validators.Length(max=64),
            validators.Required(),
        ],
    )
    password = PasswordField(
        'Password',
        [
            validators.Required(),
            validators.EqualTo('password_confirm',
                               message='Passwords must match.'),
        ],
    )
    password_confirm = PasswordField('Confirm Password')
    email = TextField(
        'E-mail',
        [
            validators.Length(max=255),
            validators.Email(),
            validators.Required(),
            validators.EqualTo('email_confirm',
                               message='E-mail addresses must match.'),
        ],
    )
    email_confirm = TextField('Confirm E-mail')


class RegisterCandidateOrVoterForm(Form):
    election_id = IntegerField(
        'Election ID',
        [
            validators.Required(),
        ],
    )
    mode = TextField(
        'Mode',
        [
            validators.AnyOf([
                'voter',
                'candidate',
            ]),
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
            flash('Welcome back, %s!' % user.name, 'success')
            # TODO: We need to make sure that 'next' points to something on our
            # site to avoid malicious redirects
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Login failed!', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template("login.html", form=form)


def logout_view():
    logout_user()
    # TODO: We need to make sure that 'next' points to something on our
    # site to avoid malicious redirects
    return redirect(request.args.get('next') or url_for('home'))


def register_view():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User.create(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        print(new_user)

        if new_user is None:
            # TODO: Put the error on the form validation instead
            # TODO: Make this still give a message afterwards, but link it to
            # the forgotten email password reset thing?
            user_exists_message = ' '.join([
                'A user called %s already exists!',
                'Please select a different username.',
            ]) % form.username.data
            flash(user_exists_message, 'danger')
            return redirect(url_for('register'))
        else:
            login_user(new_user)
            flash('Welcome to the campaign, %s!' % form.username.data,
                  'success')
            validation_message = ' '.join([
                'Your email account %s will receive a validation mail.',
                'Please click the link in that mail to validate your mail.',
            ]) % form.email.data
            flash(validation_message, 'info')
            # TODO: Redirect to /me (current user's account page)?
            return redirect(url_for('home'))
    else:
        return render_template("register.html", form=form)


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@login_required
def my_account_view():
    form = RegisterCandidateOrVoterForm(request.form)
    elections = Election.query.all()

    if request.method == 'POST' and form.validate():
        if form.mode.data == 'voter':
            voter = Voter.create(current_user.id,
                                 form.election_id.data)
            if voter is None:
                flash(
                    ('Could not vote in that election.'
                     'You may already be voter.'),
                    'danger'
                )
                return redirect(url_for('me'))
            else:
                election = [election
                            for election in elections
                            if election.id == form.election_id.data][0]
                flash(
                    ('We hope your favourite candidate wins in the %s '
                     'election in %s, %s!') % (
                            election.election_type,
                            election.location,
                            current_user.name,
                    ),
                    'success',
                )
                return redirect(url_for('me'))
        elif form.mode.data == 'candidate':
            candidate = Candidate.create(current_user.id,
                                         form.election_id.data)
            if candidate is None:
                flash(
                    ('Could not stand in that election.'
                     'You may already be standing.'),
                    'danger'
                )
                return redirect(url_for('me'))
            else:
                election = [election
                            for election in elections
                            if election.id == form.election_id.data][0]
                flash(
                    'Good luck in the %s election in %s, %s!' % (
                            election.election_type,
                            election.location,
                            current_user.name,
                    ),
                    'success',
                )
                return redirect(url_for('me'))
    try:
        user = User.query.filter(User.name == current_user.name).one()
    except NoResultFound:
        # The user does not exist, this should not happen
        flash(
            'Error accessing your account page. Please try logging in again.',
            'danger'
        )
        return redirect(url_for('home'))

    return render_template("me.html", user=user, elections=elections)
