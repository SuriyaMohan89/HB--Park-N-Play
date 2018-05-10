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











if __name__ == "__main__":

	# Set debug true so debug tool bar extension
	app.debug = True
	# templates are not cached in debug mode

	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)
	# Use the DebugToolbar
	DebugToolbarExtension(app)
	app.run(port=5000, host='0.0.0.0')


