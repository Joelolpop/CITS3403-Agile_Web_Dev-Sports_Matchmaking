from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def homepage():
    return render_template("homepage.html")







@main.route("/events/<int:event_id>")
def event_view(event_id):
    return render_template("event_view.html", event_id=event_id,user_has_joined=False)
