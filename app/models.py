from app import db
SPORTS = ["Soccer", "Basketball", "Tennis", "Netball", "Cricket", "Australian Rules Football", "Swimming", "Rugby", "Golf"]
GENDER = ["M","F","Others"]
RESPONSE_A = ["Accept", "Reject"]
RESPONSE_B = ["Accept", "Reject"]

class Users(db.Model):
    __tablename__ = 'users'
    user_id    = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(64), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name  = db.Column(db.String(64), nullable=False)
    gender     = db.Column(db.String(16), nullable=False)
    postcode   = db.Column(db.String(10), nullable=False)
    sport_1    = db.Column(db.String(64), nullable=False)
    sport_2    = db.Column(db.String(64), nullable=False)
    sport_3    = db.Column(db.String(64), nullable=False)

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


class Events(db.Model):
    __tablename__ = 'events'

    event_id          = db.Column(db.Integer, primary_key=True)
    owner_id          = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    event_name        = db.Column(db.String(128), nullable=False)
    sport             = db.Column(db.String(64), nullable=False)
    location          = db.Column(db.String(128), nullable=False)
    postcode          = db.Column(db.String(4), nullable=False)
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
        return self.owner.username if self.owner else None

class Attendees(db.Model):
    __tablename__ = 'attendees'

    id       = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    user_id  = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_host  = db.Column(db.Boolean, default=False, nullable=False)

    event = db.relationship('Events', back_populates='members')
    user  = db.relationship('Users', foreign_keys=[user_id])