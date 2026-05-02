from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def homepage():
    return render_template("homepage.html")


@main.route("/profile")
def profile():
    return render_template("user_profile_edit.html")

@main.route("/friends")
def friends_list():
    return render_template("friends_view.html")

@main.route("/friends/data")
def friend_data():
    return render_template("friend_data_view.html")


@main.route("/events")
def events_joined_available():
    return render_template(
        "event_joined_available.html")


@main.route("/events/joined-available")
def events_joined_available_alias():
    return render_template("event_joined_available.html")





@main.route("/events/<int:event_id>")
def event_view(event_id):
    return render_template("event_view.html", event_id=event_id,user_has_joined=False)

@main.route("/events/<int:event_id>/edit")
def event_edit(event_id):
    return render_template("event_edit.html", event_id=event_id)
