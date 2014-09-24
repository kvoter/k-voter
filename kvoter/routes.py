from flask import render_template, request
from flask.ext.login import login_required
from kvoter import app
from kvoter.login import login


@app.route("/")
def home_page():  # Why does this throw an exception?
    print(dir(request))
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")


app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
