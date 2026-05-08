from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Users

main = Blueprint('main', __name__)

@main.route("/")
def homepage():
    return render_template("homepage.html")


@main.route("/signup", methods=["POST"])
def signup():
    first_name = request.form.get("first_name", "").strip()
    last_name  = request.form.get("last_name", "").strip()
    email      = request.form.get("email", "").strip().lower()
    password   = request.form.get("password", "")

    if not first_name or not last_name or not email or not password:
        flash("All fields are required.", "danger")
        return redirect(url_for("main.homepage"))

    if len(password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        return redirect(url_for("main.homepage"))

    if Users.query.filter_by(email=email).first():
        flash("An account with that email already exists.", "danger")
        return redirect(url_for("main.homepage"))

    user = Users(first_name=first_name, last_name=last_name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return redirect(url_for("main.profile"))


@main.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = Users.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        flash("Invalid email or password.", "danger")
        return redirect(url_for("main.homepage"))

    login_user(user)
    return redirect(url_for("main.homepage"))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))


@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    if request.method == "POST":
        username   = request.form.get("username", "").strip() or None
        first_name = request.form.get("first_name", "").strip()
        last_name  = request.form.get("last_name", "").strip()
        gender     = request.form.get("gender", "").strip() or None
        postcode   = request.form.get("postcode", "").strip() or None
        sports     = request.form.get("sports", "").split(",")
        sports     = [s.strip() for s in sports if s.strip()]

        if not first_name or not last_name:
            flash("First and last name are required.", "danger")
            return redirect(url_for("main.profile"))

  
        if username and username != user.username:
            if Users.query.filter_by(username=username).first():
                flash("That username is already taken.", "danger")
                return redirect(url_for("main.profile"))

        user.username   = username
        user.first_name = first_name
        user.last_name  = last_name
        user.gender     = gender
        user.postcode   = postcode
        user.sport_1    = sports[0] if len(sports) > 0 else None
        user.sport_2    = sports[1] if len(sports) > 1 else None
        user.sport_3    = sports[2] if len(sports) > 2 else None

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("main.profile"))

    return render_template("user_profile_edit.html", user=user)

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

@main.route("/matching")
def matching():
    players = Users.query.all()
    return render_template("matching.html", players=players)
