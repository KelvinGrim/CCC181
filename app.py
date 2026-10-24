"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

# Sample data for the demo. It lives in memory, so it resets every time the
# server restarts. A real app would save tickets in a database later.

SERVICES = [
    {"id": 1, "name": "Deposit / Withdrawal"},
    {"id": 2, "name": "Account Openning"},
    {"id": 3, "name": "Loans"}
]

COUNTER = [

    {"id": 1, "name": "Counter 1", "service_ids": [1]},
    {"id": 2, "name": "Counter 2", "service_ids": [1, 2]},
    {"id": 3, "name": "Counter 3", "service_ids": [3]},
]

NOTIFY_AT = 3  # customer is told they are "near" when their position is 3 or less

TICKETS = [
    {"number": 1, "name": "Maria Santos", "email": "maria@example.com", "service_id": 1, "status": "called",  "counter_id": 1},
    {"number": 2, "name": "Jose Reyes",   "email": "jose@example.com",  "service_id": 3, "status": "waiting", "counter_id": None},
    {"number": 3, "name": "Ana Cruz",     "email": "ana@example.com",   "service_id": 1, "status": "waiting", "counter_id": None},
    {"number": 4, "name": "Ben Lim",      "email": "ben@example.com",   "service_id": 1, "status": "waiting", "counter_id": None},
]

@app.route("/")
def index():
    # render_template looks inside the templates/ folder and passes
    # keyword arguments to the template as variables.
    return render_template("index.html", name="Ana", tickets=TICKETS)


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    ahead = [x for x in TICKETS
             if x["service_id"] == t["service_id"]
             and x["status"] == "waiting"
             and x["number"] < t["number"]]
    service = next(s for s in SERVICES if s["id"] == t["service_id"])
    return render_template("ticket.html", ticket=t, service=service, ahead=len(ahead))

@app.post("/queue/<int:ticket_id>/leave")
def leave(ticket_id):
    t = next((t for t in TICKETS if t["number"] == ticket_id), None)
    if t is None:
        abort(404)
    t["status"] = "no-show"
    flash(f"You left the queue. Ticket #{ticket_id} was cancelled.", "info")
    return redirect(url_for("index"))


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    email = form.get("email", "").strip().lower()
    service_id = form.get("service_id", type=int)

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if "@" not in email:
        errors["email"] = "Enter a valid email address."
    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=SERVICES, form=form, errors=errors), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "email": email,
                    "service_id": service_id, "status": "waiting"})
    flash(f"You joined the queue. Your ticket is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

@app.route("/staff")
def staff_dashboard():
    return "Staff dashboard coming soon"


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
