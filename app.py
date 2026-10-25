"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

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

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
