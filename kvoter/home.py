from flask import render_template, request
from kvoter import app
from kvoter.db import Election, Candidate, User
from wtforms import Form, IntegerField, validators


class VoteForm(Form):
    election_id = IntegerField(
        'Election ID',
        [
            validators.Required(),
        ],
    )


@app.route("/")
def home_view():
    form = VoteForm(request.form)

    candidates = Candidate.query.all()
    elections = Election.query.all()
    users = {
        user.id: user
        for user in User.query.all()
    }
    elections = [
        {
            'type': election.election_type,
            'location': election.location,
            'candidates': [users[candidate.user_id]
                           for candidate in candidates
                           if candidate.election_id == election.id],
        }
        for election in elections
    ]

    if request.method == 'POST' and form.validate():
        pass

    return render_template("home.html", elections=elections)
