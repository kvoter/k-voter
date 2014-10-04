from flask import render_template
from flask.ext.login import login_required
from kvoter import app
from kvoter.auth import login_view, logout_view, register_view
from kvoter.election import create_election_view


@app.route("/")
def home_page():  # Why does this throw an exception?
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")


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
