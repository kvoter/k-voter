from flask import render_template, request, redirect, url_for
from flask.ext.login import login_required
from kvoter import app


@app.route("/")
def home_page():  # Why does this throw an exception?
    print(dir(request))
    return render_template("home.html")


@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # TODO: We need to make sure that 'next' points to something on our
        # site to avoid malicious redirects
        return redirect(request.args.get('next') or url_for('home_page'))
