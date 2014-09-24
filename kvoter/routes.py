from flask import render_template
from flask.ext.login import login_required
from kvoter import app


@app.route("/")
def home_page():  # Why does this throw an exception?
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")
