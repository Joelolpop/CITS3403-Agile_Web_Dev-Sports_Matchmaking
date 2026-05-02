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