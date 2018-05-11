""" Locate Children's park and rate"""

from jinja2 import StrictUndefined

from flask import(Flask,render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension

from model_db import User,Park,Rating,Favorite, connect_to_db,db
from sqlalchemy import update


app = Flask(__name__)

# for session encryption
app.secret_key = "asdfghjkl"

# for raising an error if undefined variable is used in jinja2
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
	"""Homepage"""

	return render_template("homepage.html")

@app.route('/register',methods=['GET'])
def register_form():
	"""Show user registration form"""

	return render_template('register_form.html')

@app.route('/register',methods=['POST'])
def register_process():
	"""Process user registration and Registers new user in the database"""

	username = request.form.get('username')
	email=request.form.get('email')
	password= request.form.get('password')
	zipcode = int(request.form.get('zipcode'))

	# session['username'] = username
	# if (User.query.filter(User.username == session[username])):
	# 	flash("Account already exists. Try Login")
	# else:
	user=User(username=username,email=email,password=password,zipcode=zipcode)
	db.session.add(user)
	db.session.commit()
	flash('Successfully Registered')
	
	return redirect('/')

@app.route('/parks')
def parks_list():
	"""Displays list of parks in San Francisco"""

	parks = Park.query.order_by(Park.parkname).all()

	return render_template("parks_list.html", parks=parks)


@app.route('/locatepark')
def locate_park():
	""" Locate a park when user types in a zip code """

	zipcode = int(request.args.get("zipcode"))
	locate_park = Park.query.filter(Park.zipcode == zipcode).all()

	return render_template("locate_park.html",locatepark=locate_park)


@app.route('/<int:park_id>' )
def view_map_park(park_id):
	"""View map of park selected by user"""
	
	print park_id
	park = Park.query.get(park_id)

	return render_template("view_map.html",park=park)











if __name__ == "__main__":

	# Set debug true so debug tool bar extension
	app.debug = True
	# templates are not cached in debug mode

	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)
	# Use the DebugToolbar
	DebugToolbarExtension(app)
	app.run(port=5000, host='0.0.0.0')


