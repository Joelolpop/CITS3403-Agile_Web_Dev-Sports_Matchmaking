from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def base():
    return render_template("base.html")

@main.route('/matching')
def matching():
    return render_template('matching.html')