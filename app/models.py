from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

SPORTS = ["Soccer", "Basketball", "Tennis", "Netball", "Cricket", "Australian Rules Football", "Swimming", "Rugby", "Golf"]
GENDER = ["M","F","Others"]
RESPONSE_A = ["Accept", "Reject"]
RESPONSE_B = ["Accept", "Reject"]

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id       = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=True)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    first_name    = db.Column(db.String(64), nullable=False)
    last_name     = db.Column(db.String(64), nullable=False)
    gender        = db.Column(db.String(16))
    postcode      = db.Column(db.Integer)
    profile_image = db.Column(db.String(255))
    instagram     = db.Column(db.String(100))
    sport_1       = db.Column(db.String(64))
    sport_2       = db.Column(db.String(64))
    sport_3       = db.Column(db.String(64))
    password_hash = db.Column(db.String(256), nullable=False)

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def sports(self):
        return [sport for sport in [self.sport_1, self.sport_2, self.sport_3] if sport]

class Matching(db.Model):
    __tablename__ = 'matching'

    matching_id = db.Column(db.Integer, primary_key=True)
    user_a_id   = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_b_id   = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    response_a  = db.Column(db.String(8))   # 'Accept' or 'Reject'
    response_b  = db.Column(db.String(8))   # 'Accept' or 'Reject'

    user_a = db.relationship('Users', foreign_keys=[user_a_id])
    user_b = db.relationship('Users', foreign_keys=[user_b_id])

    @property
    def result(self):
        if self.response_a == 'Accept' and self.response_b == 'Accept':
            return 'Friends'
        return 'Skip'


class Friends(db.Model):
    __tablename__ = 'friends'

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user   = db.relationship('Users', foreign_keys=[user_id])
    friend = db.relationship('Users', foreign_keys=[friend_id])


class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'

    id           = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    receiver_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status       = db.Column(db.String(16), nullable=False, default='pending')
    created_at   = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    requester = db.relationship('Users', foreign_keys=[requester_id])
    receiver  = db.relationship('Users', foreign_keys=[receiver_id])


class Events(db.Model):
    __tablename__ = 'events'

    event_id          = db.Column(db.Integer, primary_key=True)
    owner_id          = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_name        = db.Column(db.String(128), nullable=False)
    sport             = db.Column(db.String(64), nullable=False)
    location          = db.Column(db.String(128), nullable=False)
    postcode          = db.Column(db.Integer, nullable=False)
    description       = db.Column(db.Text)
    date              = db.Column(db.Date, nullable=False)
    time              = db.Column(db.Time, nullable=False)
    spots_total       = db.Column(db.Integer, nullable=False)

    owner   = db.relationship('Users', foreign_keys=[owner_id])
    members = db.relationship('Attendees', back_populates='event', cascade='all, delete-orphan')

    @property
    def name(self):
        return self.event_name

    @property
    def spots_filled(self):
        return len(self.members)

    @property
    def host(self):
        if self.owner:
            return self.owner.username or self.owner.first_name
        return "Unknown"

class Attendees(db.Model):
    __tablename__ = 'attendees'

    id       = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_host  = db.Column(db.Boolean, default=False, nullable=False)

    event = db.relationship('Events', back_populates='members')
    user  = db.relationship('Users', foreign_keys=[user_id])