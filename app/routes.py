from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def homepage():
    return render_template("homepage.html")


@main.route("/profile")
def profile():
    return render_template("user_profile_edit.html")

@main.route("/friends/data")
def friend_data():
    return render_template("friend_data_view.html")