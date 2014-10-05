from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from kvoter.app import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
import hashlib
from random import choice
from string import ascii_letters, digits

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kvoter.db"

db = SQLAlchemy(app)

roles_users = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    election_id = db.Column(db.Integer(), db.ForeignKey('elections.id'))

    def __init__(self, user_id, election_id):
        self.user_id = user_id
        self.election_id = election_id

    @staticmethod
    def create(user_id, election_id):
        try:
            Candidate.query.filter(
                Candidate.user_id == user_id,
                Candidate.election_id == election_id
            ).one()
            return None
        except NoResultFound:
            candidate = Candidate(user_id, election_id)
            db.session.add(candidate)
            db.session.commit()
            return candidate


#class VotersElections(db.Model):
#    __tablename__ = 'voters_elections'
#    __tableargs__ = (
#        db.UniqueConstraint('user_id', 'election_id'),
#    )
#
#    id = db.Column(db.Integer(), primary_key=True)
#    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
#    election_id = db.Column(db.Integer(), db.ForeignKey('elections.id'))


#class Vote(db.Model):
#    __tablename__ = 'votes'
#    __tableargs__ = (
#        db.UniqueConstraint('voter_id', 'candidate_id'),
#    )
#
#    id = db.Column(db.Integer(), primary_key=True)
#    voter_id = db.Column(db.Integer(), db.ForeignKey('voters_elections.id'))
#    candidate_id = db.Column(db.Integer(), db.ForeignKey('candidates_elections.id'))
#    election_id = db.Column(db.Integer(), db.ForeignKey('elections.id'))
#
#    def __init__(self, voter_id, candidate_id):
#        self.voter_id = voter_id
#        self.candidate_id = candidate_id
#
#    @staticmethod
#    def create(voter_id, candidate_id):
#        # TODO: Validate that both candidate and voter are in same election
#        try:
#            Vote.query.filter(Vote.voter_id == voter_id,
#                              Vote.candidate_id == candidate_id).one()
#            return None
#        except NoResultFound:
#            vote = Vote(voter_id, candidate_id)
#            db.session.add(vote)
#            db.session.commit()
#            return vote


class Election(db.Model):
    __tablename__ = "elections"

    id = db.Column(db.Integer(), primary_key=True)
    election_type = db.Column(db.String(80))
    location = db.Column(db.String(80))
    potential_voters = db.Column(db.Integer())
    date_of_vote = db.Column(db.DateTime())
    candidates = db.relationship('Candidate',
                                 backref='election')
    #voters = db.relationship('VotersElections',
    #                         backref='election')

    def __init__(self, election_type, location, potential_voters,
                 date_of_vote):
        self.election_type = election_type
        self.location = location
        self.potential_voters = potential_voters
        self.date_of_vote = date_of_vote

    @staticmethod
    def create(election_type, location, potential_voters, date_of_vote):
        try:
            Election.query.filter(Election.election_type == election_type,
                                  Election.location == location).one()
            return None
        except NoResultFound:
            election = Election(election_type, location, potential_voters,
                                date_of_vote)
            db.session.add(election)
            db.session.commit()
            return election


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    @staticmethod
    def get_or_create(name, description=""):
        try:
            role = Role.query.filter(Role.name == name).one()
            return role
        except NoResultFound:
            role = Role(name, description)
            db.session.add(role)
            db.session.commit()
            return role


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    _password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    created_on = db.Column(db.DateTime())
    confirmation_code = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, email, password, roles=("voter",)):
        self.name = name
        self.email = email
        self.password = password
        self.active = True
        self.confirmed_at = None
        self.created_on = datetime.now()
        self.confirmation_code = "".join(choice(ascii_letters + digits)
                                         for _ in range(32))
        for role in roles:
            role_obj = Role.get_or_create(role)
            self.roles.append(role_obj)

    @property
    def password(self):
        return self._password

    @property
    def salt(self):
        return hashlib.md5(bytes(self.name, 'utf8')).digest()

    def hash_password(self, password):
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=bytes(password, 'utf8'),
            salt=self.salt,
            iterations=100000,
        )

    @password.setter
    def password(self, password):
        self._password = self.hash_password(password)

    def is_active(self):
        # TODO: Use self.confirmed_at <= datetime.now() again?
        return self.active

    def validate_password(self, password):
        return self.password == self.hash_password(password)

    @staticmethod
    def create(name, email, password):
        try:
            User.query.filter(User.name == name).one()
            return None
        except NoResultFound:
            user = User(name, email, password)
            db.session.add(user)
            db.session.commit()
            return user
