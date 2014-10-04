from flask import render_template
from kvoter import app
from kvoter.db import Election


@app.route("/")
def home_view():
    elections = Election.query.all()
    elections = [
        {
            'type': election.election_type,
            'location': election.location,
            'candidates': [candidate
                           for candidate in election.candidates],
        }
        for election in elections
    ]

    return render_template("home.html", elections=elections)
