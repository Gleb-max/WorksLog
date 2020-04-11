import os

from flask import Flask, render_template
from data import db_session
from data.constants import DB_NAME, COLONISTS, JOBS
from data.users import User
from data.jobs import Jobs
from sqlalchemy.orm import Session


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"


@app.route("/")
@app.route("/works")
def works():
    session = db_session.create_session()
    jobs = session.query(Jobs)
    params = {
        "jobs": jobs,
        "title": "Works log",
    }
    return render_template("jobs.html", **params)


def create_users(session: Session, colonists: dict):
    for colonist in colonists:
        user = User(**colonist)
        session.add(user)
    session.commit()


def create_jobs(session: Session, jobs: dict):
    for job in jobs:
        job = Jobs(**job)
        session.add(job)
    session.commit()


def main():
    filling = not os.path.exists(DB_NAME)
    db_session.global_init(DB_NAME)
    if filling:
        session = db_session.create_session()
        create_users(session, COLONISTS)
        create_jobs(session, JOBS)
    app.run()


if __name__ == "__main__":
    main()
