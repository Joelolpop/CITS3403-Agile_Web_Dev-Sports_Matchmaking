import unittest
from app import create_app, db
from app.models import Users, Matching, Friends, FriendRequest
from app.routes import calculate_match_score
from app.config import TestConfig

def add_test_data():
    user1 = Users(
        username="testuser1",
        first_name="Albert", last_name="Einstein",
        email="albert@gmail.com", postcode=6000,
        sport_1="Tennis", sport_2="Basketball", sport_3="Soccer"
    )
    user1.set_password("password1")

    user2 = Users(
        username="testuser2",
        first_name="Isaac", last_name="Newton",
        email="isaac@gmail.com", postcode=6001,
        sport_1="Tennis", sport_2="Basketball"
    )
    user2.set_password("password2")

    user3 = Users(
        username="testuser3",
        first_name="Jason", last_name="Weenie",
        email="jason@gmail.com", postcode=6010,
        sport_1="Golf", sport_2="Rugby"
    )
    user3.set_password("password3")

    db.session.add_all([user1, user2, user3])
    db.session.commit()


