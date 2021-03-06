 ##############""" Models and Database creation Functions for Park N Play Project"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



  # Connection to PostGreSQL through Flask-SQLAlchemy helper Library

db = SQLAlchemy()


  ##################################################################################


class User(db.Model):
    """ User of Park N Play website"""

    __tablename__ = "users"


    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(75),nullable=False)
    password = db.Column(db.String(50),nullable=False)
    zipcode = db.Column(db.Integer,nullable=False)



    def __repr__(self): 
        """ For printing in Terminal,helps debugging"""

        return"<User user_id={} username={} email={} zipcode={}>".format(self.user_id,self.username,self.email,self.zipcode) #pragma: no cover



class Park(db.Model):
    """ Parks of Park N Play website"""

    __tablename__="parks"


    park_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    parkname = db.Column(db.String(50),nullable=False)
    location = db.Column(db.String(175),nullable=True)
    zipcode = db.Column(db.Integer,nullable=False)
    manager = db.Column(db.String(75),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(25),nullable=True)
    latitude = db.Column(db.Float,nullable=False)
    longitude = db.Column(db.Float,nullable=False)



    def __repr__(self):
              """ For printing in Terminal,helps debugging"""

              return "<Park park_id={} parkname={} zipcode={}>".format(self.park_id,self.parkname,self.zipcode) #pragma: no cover



class Rating(db.Model):
    """Rating score for every park"""

    __tablename__="ratings"

    rating_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    park_id = db.Column(db.Integer,db.ForeignKey('parks.park_id'))
    # user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    rating = db.Column(db.Float,nullable=False)
    reviews = db.Column(db.Integer,nullable=False)


    # user = db.relationship("User",backref=db.backref("scores",order_by=rating_id))
    park = db.relationship("Park",backref=db.backref("scores"))

    



    def __repr__(self):
        """ For printing in Terminal,helps debugging"""

        return "<Rating rating_id={} park_id={} rating={}>".format(self.rating_id,
                                                                        self.park_id,
                                                                        self.rating) #pragma: no cover


class Schedule(db.Model):
    """ Show scheduled time by user"""
    __tablename__="scheduler"

    schedule_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    park_id = db.Column(db.Integer,db.ForeignKey('parks.park_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime,nullable=False)

    user = db.relationship("User",backref=db.backref("schedule",order_by=schedule_id))
    park = db.relationship("Park",backref=db.backref("schedule",order_by=schedule_id))



    def __repr__(self):#pragma: no cover
        """ For printing in Terminal,helps debugging"""

        return "<Schedule schedule_id={} park_id={} user_id={} start_time={}>".format(self.schedule_id,
                                                                        self.park_id,
                                                                        self.user_id,
                                                                        self.start_time)








class Favorite(db.Model):
    """ Show if liked park by user"""

    __tablename__="favorites"

    favorite_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    park_id = db.Column(db.Integer,db.ForeignKey('parks.park_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    is_favorite =db.Column(db.Boolean, default = False) 

    user = db.relationship("User",backref=db.backref("favorites",order_by=favorite_id))
    park = db.relationship("Park",backref=db.backref("favorites",order_by=favorite_id))




    
    def __repr__(self):#pragma: no cover
        """ For printing in Terminal,helps debugging"""

        return "<Favorite favorite_id={} park_id={} user_id={} is_favorite={}>".format(self.favorite_id,
                                                                                    self.park_id,
                                                                                    self.user_id,
                                                                                    self.is_favorite) #pragma: no cover







        ##############################################################################################################
# Helper functions

def connect_to_db(app, default='postgresql:///childrenparks'):
    """Connect the database to our Flask app"""

    #configuration for using PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = default
    # Logs all information issued to stderr useful for debugging
    app.config['SQLALCHEMY_ECHO'] = True
    # Tracks all modifications of objects but consumes memory set false
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':

    #Help work with database directly

    from server import app
    connect_to_db(app)
    print "Connected to db"


















