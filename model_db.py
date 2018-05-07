    """ Models and Database creation Functions for Park N Play Project"""

from flask_sqlalchemy import SQLALCHEMY

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



  	def__repr__(self):
  		""" For printing in Terminal,helps debugging"""

  		return"<User user_id={} username={} email={} zipcode={}>".format(self.user_id,self.username,self.email,self.zipcode)



class Park(db.Model):
		""" Parks of Park N Play website"""

		__tablename__="parks"


		park_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
		parkname = db.Column(db.String(50),nullable=False)
		location = db.column(db.String(175),nullable=True)
		zipcode = db.Column(db.Integer,nullable=False)
		manager = db.Column(db.String(75),nullable=False)
		email = db.Column(db.String(100),nullable=False)
		phone = db.Column(db.String(25),nullable=True)



		def__repr__(self):
  		          """ For printing in Terminal,helps debugging"""

  		          return "<Park park_id={} parkname={} zipcode={}>".format(self.park_id,self.parkname,self.zipcode)



class Rating(db.Model):
	"""Rating score for every park"""

	__tablename__="ratings"

	rating_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	park_id = db.Column(db.Integer,
                        db.ForeignKey('parks.park_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer, nullable=False)


     def __repr__(self):
  		          """ For printing in Terminal,helps debugging"""

        return "<Rating rating_id={} park_id={} user_id={} score={}>".format(self.rating_id,
                                                                           self.park_id,
                                                                           self.user_id,
                                                                           self.score)



class Favorite(db.Model):
	""" Show if liked park by user"""

	__tablename__="favorites"

	favorite_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
	park_id = db.Column(db.Integer,
                        db.ForeignKey('parks.park_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))






