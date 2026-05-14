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
        sport_1="Swimming", sport_2="Basketball"
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

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = Users.query.filter_by(email="albert@gmail.com").first()
        self.assertTrue(user.check_password("password1"))
        self.assertFalse(user.check_password("wrongpassword"))
    
    def test_sports_property(self):
        user = Users.query.filter_by(email="albert@gmail.com").first()
        self.assertEqual(user.sport_1, "Tennis")
        self.assertEqual(user.sport_2, "Basketball")
        self.assertEqual(user.sport_3, "Soccer")
        self.assertEqual(user.sports, ["Tennis", "Basketball", "Soccer"])
    
    def test_get_id(self):
        user = Users.query.filter_by(email="albert@gmail.com").first()
        self.assertIsInstance(user.get_id(), str)

class MatchingScoreTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_match_score_one_common_sport(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        #Albert and Isaac have 1 common sport (Basketball) and are 1 postcode apart
        score = calculate_match_score(user1, user2)
        self.assertEqual(score, 3)
    
    def test_match_score_no_common_sport(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user3 = Users.query.filter_by(email="jason@gmail.com").first()

        #Albert and Jason have no common sports and are 10 postcodes apart
        score = calculate_match_score(user1, user3)
        self.assertEqual(score, 13)
    
    def test_match_score_no_postcode(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()

        user_no_postcode = Users(
            username="nopostcode",
            first_name="No", last_name="Postcode",
            email="nopost@gmail.com", sport_1 = "Tennis"
        )
        user_no_postcode.set_password("nopassword")
        db.session.add(user_no_postcode)
        db.session.commit()

        score = calculate_match_score(user1, user_no_postcode)

        #check if missing postcode is handled correctly

        self.assertIsNotNone(score)


