"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, redirect, render_template, request, url_for

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


@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    for position, t in enumerate(TICKETS, start=1):
        if t["number"] == ticket_id:
            return render_template("ticket.html", ticket=t, position=position)
    abort(404)  # no ticket with that number


@app.route("/join", methods=["GET", "POST"])
def join():
    # GET: show the empty form. POST: the form was submitted.
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            return render_template("join.html", error="Please enter your name.")

        number = TICKETS[-1]["number"] + 1 if TICKETS else 1
        TICKETS.append({"number": number, "name": name})
        # Redirect after POST so refreshing the page doesn't join twice.
        return redirect(url_for("ticket", ticket_id=number))

    return render_template("join.html")


@app.route("/join")
def join_form():
    return render_template("join.html")

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
