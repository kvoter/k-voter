from kvoter import app
from kvoter.auth import (login_view, logout_view, register_view,
                         my_account_view)
from kvoter.election import create_election_view
from kvoter.home import home_view

app.add_url_rule(
    '/',
    'home',
    home_view,
    methods=['GET', 'POST'],
)
app.add_url_rule(
    '/login',
    'login',
    login_view,
    methods=['GET', 'POST'],
)
app.add_url_rule(
    '/logout',
    'logout',
    logout_view,
)
app.add_url_rule(
    '/register',
    'register',
    register_view,
    methods=['GET', 'POST'],
)
app.add_url_rule(
    '/create_election',
    'create_election',
    create_election_view,
    methods=['GET', 'POST'],
)
app.add_url_rule(
    '/me',
    'me',
    my_account_view,
    methods=['GET', 'POST'],
)
