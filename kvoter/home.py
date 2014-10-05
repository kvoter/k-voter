from flask import render_template
from kvoter import app
from kvoter.db import Election, Candidate, User


@app.route("/")
def home_view():
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

    return render_template("home.html", elections=elections)
