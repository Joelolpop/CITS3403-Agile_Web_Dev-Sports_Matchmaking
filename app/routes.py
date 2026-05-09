import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Users, Matching, Friends, Events, Attendees
import datetime

main = Blueprint('main', __name__)

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg"}

PUBLIC_ENDPOINTS = {
    "main.homepage",
    "main.login",
    "main.signup",
}


@main.before_app_request
def require_login_for_protected_routes():
    if current_user.is_authenticated:
        return None

    if request.endpoint is None:
        return None

    if request.endpoint.startswith("static") or request.endpoint in PUBLIC_ENDPOINTS:
        return None

    return redirect(url_for("main.homepage"))

def calculate_match_score(current_user, other_user):
    current_sports = set(filter(None, [
        current_user.sport_1,
        current_user.sport_2,
        current_user.sport_3
    ]))
    other_sports = set(filter(None, [
        other_user.sport_1,
        other_user.sport_2,
        other_user.sport_3
    ]))

    common_sports = len(current_sports & other_sports)
    sport_score = 3 - common_sports

    try:
        postcode_score = abs(int(current_user.postcode) - int(other_user.postcode))
    except (ValueError, TypeError):
        postcode_score = 9999

    total_score = sport_score + postcode_score
    return total_score


def parse_postcode(raw_postcode, required=True):
    postcode = (raw_postcode or "").strip()

    if not postcode:
        if required:
            return None, "Postcode is required."
        return None, None

    if not postcode.isdigit() or len(postcode) != 4:
        return None, "Postcode must be exactly 4 digits."

    return int(postcode), None


def allowed_image_filename(filename):
    if not filename:
        return False
    extension = os.path.splitext(filename)[1].lower()
    return extension in ALLOWED_IMAGE_EXTENSIONS

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
        postcode_raw = request.form.get("postcode", "")
        instagram  = request.form.get("instagram", "").strip() or None
        sports     = request.form.get("sports", "").split(",")
        sports     = [s.strip() for s in sports if s.strip()]
        profile_image = request.files.get("profile_image")

        if not first_name or not last_name:
            flash("First and last name are required.", "danger")
            return redirect(url_for("main.profile"))

  
        if username and username != user.username:
            if Users.query.filter_by(username=username).first():
                flash("That username is already taken.", "danger")
                return redirect(url_for("main.profile"))

        postcode, postcode_error = parse_postcode(postcode_raw, required=False)
        if postcode_error:
            flash(postcode_error, "danger")
            return redirect(url_for("main.profile"))

        if profile_image and profile_image.filename:
            if not allowed_image_filename(profile_image.filename):
                flash("Profile image must be a .jpg or .jpeg file.", "danger")
                return redirect(url_for("main.profile"))

        user.username   = username
        user.first_name = first_name
        user.last_name  = last_name
        user.gender     = gender
        user.postcode   = postcode
        user.instagram  = instagram

        if profile_image and profile_image.filename:
            filename = secure_filename(profile_image.filename)
            upload_folder = os.path.join(current_app.root_path, "static", "uploads", "profiles")
            os.makedirs(upload_folder, exist_ok=True)

            stored_filename = f"user_{user.user_id}.jpg"
            profile_image.save(os.path.join(upload_folder, stored_filename))
            user.profile_image = f"uploads/profiles/{stored_filename}"

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

@main.route("/events/create", methods=["POST"])
@login_required
def create_event():
    event_name  = request.form.get("event_name", "").strip()
    sport       = request.form.get("sport", "").strip()
    location    = request.form.get("location", "").strip()
    postcode_raw = request.form.get("postcode", "")
    description = request.form.get("description", "").strip()
    date_str    = request.form.get("date", "")
    time_str    = request.form.get("time", "")
    spots_total = request.form.get("spots_total", "")

    if not all([event_name, sport, location, postcode_raw, date_str, time_str, spots_total]):
        flash("All fields except description are required.", "danger")
        return redirect(url_for("main.homepage"))

    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.datetime.strptime(time_str, "%H:%M").time()
        spots_total = int(spots_total)
        if spots_total < 1:
            raise ValueError
    except ValueError:
        flash("Invalid date, time, or spots value.", "danger")
        return redirect(url_for("main.homepage"))
    
    postcode, postcode_error = parse_postcode(postcode_raw, required=True)
    if postcode_error:
        flash(postcode_error, "danger")
        return redirect(url_for("main.homepage"))

    event = Events(
        owner_id    = current_user.user_id,
        event_name  = event_name,
        sport       = sport,
        location    = location,
        postcode    = postcode,
        description = description,
        date        = date,
        time        = time,
        spots_total = spots_total
    )
    db.session.add(event)
    db.session.flush()

    host = Attendees(
        event_id = event.event_id,
        user_id  = current_user.user_id,
        is_host  = True
    )
    db.session.add(host)
    db.session.commit()

    return redirect(url_for("main.event_view", event_id=event.event_id))


@main.route("/events/joined-available")
def events_joined_available_alias():
    return render_template("event_joined_available.html")


@main.route("/events/<int:event_id>")
@login_required
def event_view(event_id):
    event = Events.query.get_or_404(event_id)
    user_has_joined = Attendees.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first() is not None

    return render_template("event_view.html", event=event, user_has_joined=user_has_joined)

@main.route("/events/<int:event_id>/join")
@login_required
def event_join(event_id):
    event = Events.query.get_or_404(event_id)

    already_joined = Attendees.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()

    if already_joined:
        flash("You have already joined this event.", "warning")
        return redirect(url_for("main.event_view", event_id=event_id))

    if event.spots_filled >= event.spots_total:
        flash("This event is full.", "danger")
        return redirect(url_for("main.event_view", event_id=event_id))
    
    attendee = Attendees(
        event_id = event_id,
        user_id  = current_user.user_id,
        is_host  = False
    )
    db.session.add(attendee)
    db.session.commit()

    flash("You have joined the event!", "success")
    return redirect(url_for("main.event_view", event_id=event_id))

@main.route("/events/<int:event_id>/leave")
@login_required
def event_leave(event_id):
    attendee = Attendees.query.filter_by(
        event_id=event_id,
        user_id=current_user.user_id
    ).first()

    if not attendee:
        flash("You are not part of this event.", "warning")
        return redirect(url_for("main.event_view", event_id=event_id))

    if attendee.is_host:
        flash("You are the host and cannot leave your own event.", "danger")
        return redirect(url_for("main.event_view", event_id=event_id))

    db.session.delete(attendee)
    db.session.commit()

    flash("You have left the event.", "success")
    return redirect(url_for("main.event_view", event_id=event_id))


@main.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def event_edit(event_id):
    event = Events.query.get_or_404(event_id)

    if event.owner_id != current_user.user_id:
        flash("You are not the host of this event.", "danger")
        return redirect(url_for("main.event_view", event_id=event_id))

    if request.method == "POST":
        event_name  = request.form.get("event_name", "").strip()
        sport       = request.form.get("sport", "").strip()
        location    = request.form.get("location", "").strip()
        postcode    = request.form.get("postcode", "").strip()
        description = request.form.get("description", "").strip()
        date_str    = request.form.get("date", "")
        time_str    = request.form.get("time", "")
        spots_total = request.form.get("spots_total", "")

        if not all([event_name, sport, location, postcode, date_str, time_str, spots_total]):
            flash("All fields except description are required.", "danger")
            return redirect(url_for("main.event_edit", event_id=event_id))

        if not postcode.isdigit() or len(postcode) != 4:
            flash("Postcode must be exactly 4 digits.", "danger")
            return redirect(url_for("main.event_edit", event_id=event_id))

        try:
            event.date        = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            event.time        = datetime.datetime.strptime(time_str, "%H:%M").time()
            event.spots_total = int(spots_total)
            if event.spots_total < 1:
                raise ValueError
        except ValueError:
            flash("Invalid date, time, or spots value.", "danger")
            return redirect(url_for("main.event_edit", event_id=event_id))

        event.event_name  = event_name
        event.sport       = sport
        event.location    = location
        event.postcode    = postcode
        event.description = description

        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for("main.event_view", event_id=event_id))

    return render_template("event_edit.html", event=event)

@main.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def event_delete(event_id):
    event = Events.query.get_or_404(event_id)

    if event.owner_id != current_user.user_id:
        flash("You are not the host of this event.", "danger")
        return redirect(url_for("main.event_view", event_id=event_id))

    db.session.delete(event)
    db.session.commit()

    flash("Event deleted.", "success")
    return redirect(url_for("main.homepage"))

@main.route("/matching")
@login_required
def matching():
    existing_friends = Friends.query.filter_by(user_id=current_user.user_id).all()
    friends_ids = {f.friend_id for f in existing_friends}
    friends_ids.add(current_user.user_id)

    candidates = Users.query.filter(Users.user_id.notin_(friends_ids)).all()
    scored = sorted(candidates, key=lambda u: calculate_match_score(current_user, u))

    return render_template("matching.html", matches=scored)
