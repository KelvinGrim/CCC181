"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import re

from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Service, Ticket, User, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)
# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.






NOTIFY_AT = 3  # customer is told they are "near" when their position is 3 or less


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    queue = [x for x in TICKETS if x["status"] in ("waiting", "called")]
    ahead = [x for x in queue
             if x["status"] == "waiting" and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])

    position = len(ahead) + 1
    near = t["status"] == "waiting" and position <= NOTIFY_AT

    return render_template("ticket.html", ticket=t, service=service,
                           ahead=len(ahead), queue=queue, near=near)


@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash(f"You left the queue. Ticket #{ticket_id} was cancelled.", "info")
    return redirect(url_for("index"))


def all_services():
    return db.session.scalars(
        db.select(Service).where(Service.is_active).order_by(Service.name)
    ).all()


@app.get("/join")
def join_form():
    return render_template("join.html", services=all_services(), form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)
    service = db.session.get(Service, service_id) if service_id else None

    errors = {}
    if not name or len(name) > 100:
        errors["name"] = "Enter your name (up to 100 characters)."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+", email) or len(email) > 120:
        errors["email"] = "Enter a valid email address."
    if service is None or not service.is_active:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors=errors), 400

    user = db.session.scalar(db.select(User).filter_by(email=email))
    if user is None:
        user = User(name=name, email=email)
    else:
        user.name = name
    ticket = Ticket(user=user, service=service)
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=all_services(),
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your ticket is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))

@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    queue = [t for t in TICKETS if t["status"] in ("waiting", "called")]
    if service_id:
        queue = [t for t in queue if t["service_id"] == service_id]
    names = {s["id"]: s["name"] for s in SERVICES}

    current = next((t for t in queue if t["status"] == "called"), None)
    up_next = next((t for t in queue if t["status"] == "waiting"), None)

    # ★ feature: how many are waiting per service
    waiting_counts = {s["name"]: sum(1 for t in TICKETS
                                     if t["status"] == "waiting" and t["service_id"] == s["id"])
                      for s in SERVICES}

    return render_template("staff.html", queue=queue, services=SERVICES, names=names,
                           selected=service_id, current=current, up_next=up_next,
                           waiting_counts=waiting_counts)


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"call": "called", "serve": "served", "no-show": "no-show"}.get(action)
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None or new_status is None:
        abort(404)

    # Finish the current customer before calling someone else
    if action == "call" and any(x["status"] == "called" for x in TICKETS):
        flash("Mark the current ticket as Served or No-show before calling the next one.", "warning")
        return redirect(url_for("staff_dashboard"))

    t["status"] = new_status
    flash(f"Ticket #{ticket_id} marked {new_status}.", "info")
    return redirect(url_for("staff_dashboard"))

@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    queue = [x for x in TICKETS if x["status"] in ("waiting", "called")]
    ahead = len([x for x in queue
                 if x["status"] == "waiting" and x["number"] < t["number"]])
    near = t["status"] == "waiting" and ahead + 1 <= NOTIFY_AT
    return jsonify(status=t["status"], ahead=ahead, near=near,
                   queue=[[x["number"], x["status"]] for x in queue])

@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"

@app.cli.command("seed")
def seed():
    """Add the starting services if they are not there yet."""
    starting = [
        ("Deposit / Withdrawal", 5, None),
        ("Account Opening", 15, "Bring a valid ID"),
        ("Loans", 20, None),
    ]
    for name, minutes, notice in starting:
        exists = db.session.scalar(db.select(Service).filter_by(name=name))
        if exists is None:
            db.session.add(Service(name=name, avg_minutes=minutes, notice=notice))
    db.session.commit()
    print("Services are ready.")
if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
