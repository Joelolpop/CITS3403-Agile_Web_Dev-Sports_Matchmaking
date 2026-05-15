import unittest
from app import create_app, db
from app.models import Users, Matching, Friends, FriendRequest
from app.routes import calculate_match_score, create_friend_pair
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

class MatchingModelTestCase(unittest.TestCase):

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

    def test_matching_both_accept(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        match = Matching(user_a_id=user1.user_id, user_b_id=user2.user_id, response_a='Accept', response_b='Accept')

        db.session.add(match)
        db.session.commit()

        self.assertEqual(match.result, 'Friends')

    def test_matching_one_reject(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        match = Matching(user_a_id=user1.user_id, user_b_id=user2.user_id, response_a='Accept', response_b='Reject')

        db.session.add(match)
        db.session.commit()

        self.assertEqual(match.result, 'Skip')
    
    def test_matching_both_reject(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        match = Matching(user_a_id=user1.user_id, user_b_id=user2.user_id, response_a='Reject', response_b='Reject')

        db.session.add(match)
        db.session.commit()

        self.assertEqual(match.result, 'Skip')

    def test_matching_first_rejects(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        match = Matching(user_a_id=user1.user_id, user_b_id=user2.user_id, response_a='Reject', response_b='Accept')

        db.session.add(match)
        db.session.commit()

        self.assertEqual(match.result, 'Skip')

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_page(self):
        response = self.client.post('/signup', data={
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@gmail.com",
            "password": "newpassword"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        user = Users.query.filter_by(email="newuser@gmail.com").first()
        self.assertIsNotNone(user)
    
    def test_login_page(self):
        response = self.client.post('/login', data={
            "email": "albert@gmail.com",
            "password": "password1"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_friends_search_json(self):
        self.client.post('/login', data={
            "email": "albert@gmail.com",
            "password": "password1"
        }, follow_redirects=True)

        response = self.client.get('/friends/search?q=isaac')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('friends', data)

class FriendRequestModelTestCase(unittest.TestCase):

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

    def test_friend_request_status(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        friend_request = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request)
        db.session.commit()
        self.assertEqual(friend_request.status, "pending")

        friend_request.status = "accepted"
        db.session.commit()
        self.assertEqual(friend_request.status, "accepted")

        FriendRequest.query.filter_by(requester_id=user1.user_id, receiver_id=user2.user_id).delete()

        friend_request = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request)
        db.session.commit()

        friend_request.status = "rejected"
        db.session.commit()
        self.assertEqual(friend_request.status, "rejected")

    def test_friend_request_duplicate(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        friend_request1 = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request1)
        db.session.commit()

        friend_request2 = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request2)
        #Check that adding a duplicate friend request return ok as False
        self.assertFalse(db.session.commit())
    
    def test_self_friend_request(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()

        friend_request = FriendRequest(requester_id=user1.user_id, receiver_id=user1.user_id, status="pending")
        db.session.add(friend_request)

        #Check that adding a self friend request return ok as False
        self.assertFalse(db.session.commit())
    
    def test_friend_request_relationships(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        friend_request = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request)
        db.session.commit()

        self.assertEqual(friend_request.requester, user1)
        self.assertEqual(friend_request.receiver, user2)
    
    def test_friend_request_acceptance_creates_friendship(self):
        user1 = Users.query.filter_by(email="albert@gmail.com").first()
        user2 = Users.query.filter_by(email="isaac@gmail.com").first()

        friend_request = FriendRequest(requester_id=user1.user_id, receiver_id=user2.user_id, status="pending")
        db.session.add(friend_request)
        db.session.commit()

        friend_request.status = "accepted"
        create_friend_pair(user1.user_id, user2.user_id)
        db.session.commit()

        friendship = Friends.query.filter_by(user_id=user1.user_id, friend_id=user2.user_id).first()
        self.assertIsNotNone(friendship)

        
            

if __name__ == '__main__':
    unittest.main()