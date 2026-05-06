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
