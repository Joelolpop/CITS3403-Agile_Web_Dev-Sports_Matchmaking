from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def homepage():
    return render_template("homepage.html")


@main.route("/profile")
def profile():
    return render_template("user_profile_edit.html")








@main.route("/events/<int:event_id>")
def event_view(event_id):
    event = {
        "id": 1,
        "name": "Tennis at UWA",
        "sport": "Tennis",
        "host": "alexsmith",
        "date": "Sat 3 May 2026",
        "time": "10:00 AM",
        "location": "Nedlands",
        "postcode": 6009,
        "description": "Casual doubles at the UWA courts. All skill levels welcome. Bring your own racket if you have one, balls provided.",
        "spots_total": 10,
        "spots_filled": 3,
        "attendees": [
            {"name": "alexsmith", "is_host": True},
            {"name": "jake_p", "is_host": False},
            {"name": "Sara92", "is_host": False},
        ]
        
    }
    return render_template("event_view.html", event=event, user_has_joined=False)

@main.route("/events/<int:event_id>/edit")
def event_edit(event_id):
    event = {
        "id": 1,
        "name": "Tennis at UWA",
        "sport": "Tennis",
        "date": "2026-05-03",
        "time": "10:00",
        "location": "Nedlands",
        "postcode": 6009,
        "description": "Casual doubles at the UWA courts. All skill levels welcome. Bring your own racket if you have one, balls provided.",
        "spots_total": 10,
    }
    return render_template("event_edit.html", event=event)