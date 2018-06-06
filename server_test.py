from unittest import TestCase
from server import app
from model_db import connect_to_db,db,Park, User, Rating, Schedule
from seed_db import load_parks
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] =  "asdfghjkl"
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2


        park1 = Park(park_id = 90, parkname = "JACKSON PLAYGROUND", location = "17th,San Francisco, CA,", zipcode = "94107", latitude = "32.87", longitude = "-122.45", email = "ar", phone = " ", manager = " ")
        park2 = Park(park_id = 100, parkname = "JOSEPH LEE RECREATION CENTER", location = "1395 Mendell St,San Francisco, CA,", zipcode = "94107", latitude = "32.87", longitude = "-122.45", email = "ar", phone = " ", manager = " ")
        user1 = User(user_id = 2, username = "maxwell73", email = "danielle29@gmail.com", password = "Test123$", zipcode = "49443")
        user2 = User(user_id = 3, username = "swu ", email = "chasehenry@yahoo.com", password = "Test123$", zipcode = "90869")
        rating1 = Rating(rating_id =2, park_id=90, rating=4, reviews=1)
        schedule1 = Schedule(schedule_id = 2, park_id=90, user_id= 2,start_time="2018-06-06 16:00:00",  end_time="2018-06-06 19:00:00")
        schedule2 = Schedule(schedule_id = 3, park_id=90, user_id= 3,start_time="2018-06-07 13:00:00",  end_time="2018-06-06 15:00:00")

        db.session.add(park1)
        db.session.add(park2)
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(schedule1)
        db.session.add(schedule2)
        db.session.commit

    def test_homepage(self):
        """Test homepage"""
        print "Homepage"
        result = self.client.get("/")
        self.assertIn("Parks", result.data)

    def test_register_form(self):
        """Test register form"""
        print "Register form"
        result = self.client.get("/register")
        self.assertIn("Username",result.data)

    def test_register_process(self):
        """Test Register Process"""
        result = self.client.post("/register", data={"username": "Mohan", "email":"mohan@mail.com", "password1": "Test123$", "password2": "Test123$", "zipcode": "94107"}, follow_redirects=True)
        self.assertIn("Successfully", result.data)

    def test_register_incorrect(self):
        """ Test for Incorrect password"""

        result = self.client.post("/register", data={ "username" : "maxwell73", "email" : "danielle29@mail.com", "password1" : "Test123$", "password2" : "Test123!!!", "zipcode" : "49443"}, follow_redirects=True)
        self.assertIn("Incorrect password",result.data)


    def test_register_exists(self):
        """Test to check if user already exists"""

        result = self.client.post("/register", data={ "username" : "maxwell73", "email" : "danielle29@gmail.com", "password1" : "Test123$", "password2" : "Test123$", "zipcode" : "49443"}, follow_redirects=True)
        self.assertIn("Account already exists",result.data)
# ###########################################################################

    def test_login_form(self):
        """Test Login Form"""
        result = self.client.get("/login")
        self.assertIn("password",result.data)

    def test_login_process(self):
        """Test login Process"""

        result = self.client.post("/login",data={"username":"Mohan", "password":"Test123$"},follow_redirects=True)
        self.assertIn("Incorrect",result.data)

    def test_login_success(self):
        """Test user details are correct """

        result = self.client.post("/login",data={"username":"maxwell73", "password":"Test123$"},follow_redirects=True)
        self.assertIn("Successfully",result.data)

    def test_login_session(self):
        """Test to check if session works"""

        result = self.client.post("/login", data={"username":"djohnson", "password" : "Test123$" }, follow_redirects=True)
        self.assertIn("Incorrect", result.data)


    def test_login_json(self):
        """Test if returns jsonified result"""

        result = self.client.get("/login.json",query_string={"zipcode" : "94107"}) 
        self.assertIs(type(result.data),str)

    def test_login_json_parklist(self):
        """Test if returns a jsonified result"""

        result = self.client.get("/login.json",query_string={"zipcode" : "94107"}) 
        self.assertIn("JACKSON PLAYGROUND",result.data)


    def test_login_json(self):
        """Test login details"""

        result = self.client.get("/login.json", query_string={"zipcode" : "52152"},follow_redirects=True)
        self.assertIn("Park not found", result.data)

# # ###################################################################################3

    def test_logout(self):
        """If user has logged out"""
        result = self.client.get("/logout",follow_redirects=True)
        self.assertIn("logged out", result.data) 

# ######################################################################################

    def test_parks(self):
        """Test parks display"""

        result = self.client.get("/parks")
        self.assertIn("Parks",result.data)

    def test_park_info(self):
        """Test parks info"""
        result = self.client.get('/parks/90', query_string = {"parkname": "JACKSON PLAYGROUND"})
        self.assertIn("Add",result.data)
# # #############################################################################


    def test_park_ratings(self):
        """Test for ratings"""

        result = self.client.get("/parks/90/edit", query_string={"cleanscore":5, "equipscore":4, "maintainscore":4},follow_redirects=True)
        self.assertIn("4", result.data)

    def test_park_ratings_flash(self):
        """Test for ratings"""

        result = self.client.get("/parks/90/edit", query_string={"cleanscore":5, "equipscore":4, "maintainscore":4},follow_redirects=True)
        self.assertIn("Thanks for feedback", result.data)


    def test_park_ratings_ratedpark(self):
        """Test for ratings which is already rated"""

        result = self.client.get("/parks/90/edit", query_string={"cleanscore":1, "equipscore":1, "maintainscore":1},follow_redirects=True) 
        self.assertIn("3", result.data)

    def test_park_ratings_reviews(self):
        """Test reviews"""

        result = self.client.get("/parks/100/edit", query_string={"cleanscore":5, "equipscore":4, "maintainscore":4},follow_redirects=True)
        self.assertIn("1", result.data)

# # #######################################################################
    
    def test_locate_park(self):
        """Test locate Park"""

        result = self.client.get("/locatepark", query_string={"zipcode" : "94107"},follow_redirects=True)
        self.assertIn("Parks",result.data)

    def test_park_not_found(self):
        """Test if the park is not found flash"""

        result = self.client.get("/locatepark", query_string={"zipcode" : "12345"},follow_redirects=True)
        self.assertIn("park not found",result.data)

    def test_locate_park_suggestions(self):
        """Test zipcode suggestions"""

        result = self.client.get("/locatepark", query_string={"zipcode" : "94106"},follow_redirects=True)
        self.assertIn("Suggestions",result.data)
# #######################################################################################################################


    def test_schedule(self):
        """Test If schedule works"""

        result = self.client.get('/schedule/90', query_string = {"parkname": "JACKSON PLAYGROUND"})
        self.assertIn("Select Park",result.data)

    def test_schedule_format(self):
        """Test if date is in right format"""

        result = self.client.get('/schedule/90/schedule.json', query_string = {"start_date": "Fri Jun 01 2018 12:00:00 GMT-0700 (PDT)", "end_date": "Fri Jun 01 2018 13:00:00 GMT-0700 (PDT)"})
        self.assertIn("reschedule",result.data)

    def test_schedule_feature(self):
        """Test schedule"""

        result = self.client.get('/schedule/90/schedule.json', query_string = {"start_date": "Wed Jun 06 2018 16:00:00 GMT-0700 (PDT)", "end_date": "Wed Jun 06 2018 19:00:00 GMT-0700 (PDT)"},follow_redirects=True)
        self.assertIs(type(result.data), str)

    def test_schedule_feature_suggestions(self):
        """Test schedule options"""

        result = self.client.get('/schedule/90/schedule.json', query_string = {"start_date": "Wed Jun 07 2018 16:00:00 GMT-0700 (PDT)", "end_date": "Wed Jun 07 2018 19:00:00 GMT-0700 (PDT)"},follow_redirects=True)
        self.assertIs(type(result.data), str)

    def test_schedule_feature_suggestions(self):
        """Test schedule suggestion query"""

        result = self.client.get('/schedule/90/schedule.json', query_string = {"start_date": "Wed Jun 07 2018 16:00:00 GMT-0700 (PDT)", "end_date": "Wed Jun 07 2018 19:00:00 GMT-0700 (PDT)"},follow_redirects=True)
        self.assertIn("0",result.data )
 


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    


if __name__ == "__main__":
    import unittest

    unittest.main()
