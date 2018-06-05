from unittest import TestCase
from server import app
from model_db import connect_to_db,db,Park
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
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        # park1 = Park(park_id = 90, parkname = "JACKSON PLAYGROUND", location = "17th,San Francisco, CA,", zipcode = "94107", latitude = "32.87", longitude = "-122.45", email = "ar", phone = " ", manager = " ")
        # db.session.add(park1)
        # db.session.commit
        # load_parks()



    # def test_homepage(self):
    #   """Test homepage"""
    #   print "Homepage"
    #   result = self.client.get("/")
    #   self.assertIn("Parks", result.data)

    # def test_register_form(self):
    #   """Test register form"""
    #   print "Register form"
    #   result = self.client.get("/register")
    #   self.assertIn("Username",result.data)

    # def test_register_process(self):
    #   """Test Register Process"""
    #   result = self.client.post("/register", data={"username": "Mohan", "email":"mohan@mail.com", "password1": "Test123$", "password2": "Test123$", "zipcode": int("94107")}, follow_redirects=True)
    #   self.assertIn("Successfully", result.data)

    # def test_login_form(self):
    #   """Test Login Form"""
    #   result = self.client.get("/login")
    #   self.assertIn("password",result.data)

    # def test_login_process(self):
    #   """Test login Process"""

    #   result = self.client.post("/login", data={"username":"Mohan", "password":"Test123$"},follow_redirects=True)
    #   self.assertIn("park",result.data)

    # def test_parks(self):
    #   """Test parks display"""

    #   result = self.client.get("/parks")
    #   self.assertIn("Parks",result.data)

    # def test_park_info(self):
    #     """Test parks info"""
    #     result = self.client.get('/parks/90', query_string = {"parkname": "JACKSON PLAYGROUND"})
    #     self.assertIn("Add",result.data)

    # def test_login_json(self):
    #   """Test login details"""

    #     result = self.client.get("/login.json", query_string={"zipcode" : "94107"})
    
    # def test_locate_park(self):
    #     """Test locate Park"""

    #     result = self.client.get("/locatepark", query_string={"zipcode" : "94107"},follow_redirects=True)
    #     print "!!!!!!!!!!!!!!!!!!!!!!!!"
    #     print type(result.data)
        # self.assertIn("Parks",result.data)      

    def test_schedule(self):
        """Test If schedule works"""

        result = self.client.get('/schedule/90', query_string = {"parkname": "JACKSON PLAYGROUND"})
        self.assertIn("Select Park",result.data)


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    


if __name__ == "__main__":
    import unittest

    unittest.main()
