from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def base():
    return render_template("base.html")