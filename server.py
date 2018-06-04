""" Locate Children's park and rate"""

from jinja2 import StrictUndefined

from flask import(Flask,render_template, redirect, request, flash, session, url_for)
from flask_debugtoolbar import DebugToolbarExtension

from model_db import User,Park,Rating,Favorite,Schedule,connect_to_db,db
from sqlalchemy import update
from flask import jsonify 
from flask import json
from datetime import date,time,datetime


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
	password= request.form.get('password1')
	confirm_password = request.form.get('password2')
	zipcode = int(request.form.get('zipcode'))

	if (User.query.filter(User.username == username,User.email == email)).first():
		flash("Account already exists. Try Login")
	else:
		if password == confirm_password :
			user=User(username=username,email=email,password=password,zipcode=zipcode)
			db.session.add(user)
			db.session.commit()
			flash('Successfully Registered')
		else:
			flash("Incorrect password.")
	
	return redirect('/')

@app.route("/login",methods=["GET"])
def login_form():
	"""Show Login page"""

	return render_template("login_page.html")


@app.route('/login',methods=['POST'])
def login_process():
	"""Process Login form"""
	login = request.form.get('username')
	password = request.form.get('password')
	user = User.query.filter(((User.email == login) | (User.username == login)) & (User.password == password)).first()
	if user:
		session["user_id"] = user.user_id
		flash("Successfully Logged In!!")
		return render_template('user_info.html',user=user)

	else:
		flash("Incorrect Login details")
		return redirect('/login')


@app.route('/login.json')
def search_park():
	""" Search park by zipcode for ratings."""
	zipcode = int(request.args.get('zipcode'))
	search_park = Park.query.filter(Park.zipcode == zipcode).all()

	park_dict = {}
	if search_park:
		for park in search_park:
			park_dict[park.zipcode] = [park.park_id,park.parkname,park.location, park.manager, park.email, park.phone]
	print search_park
	park_list =[]
	park_dict = {}
	if search_park:
		for park in search_park:
			temp = [park.park_id,park.parkname,park.location,park.manager,park.email,park.phone]
			park_list.append(temp)

		return jsonify(park_list)
	else:
		flash('Park not found in zipcode.Try another zipcode')


@app.route('/schedule/<int:park_id>')
def schedule(park_id):
	"""Schedule to find play mate"""

	return render_template("schedule.html", park_id = park_id)

@app.route('/schedule/<int:park_id>/schedule.json')
def schedule_process(park_id):
	"""Given the start time and end time query for correlations"""
	
	date_start = str(request.args.get("start_date"))
	date_end = str(request.args.get("end_date"))
	start_str = date_start[0:-14]
	start_str = start_str.rstrip()
	end_str = date_end[0:-14]
	end_str = end_str.rstrip()
	try:
		start_time = datetime.strptime(start_str,"%a %b %d %Y %H:%M:%S")
		# print "~~~~~~~~~~~~~~~~~~"
		# print start_time
		end_time = datetime.strptime(end_str,"%a %b %d %Y %H:%M:%S")
		# print "~~~~~~~~~~~~~~~~~~"
		# print end_time

	except ValueError:
	 	print("Incorrect data format, should be YYYY-MM-DD")

	if start_time > datetime.now():
		schedule = Schedule(park_id =park_id, user_id = session["user_id"], start_time=start_time, end_time=end_time)
		print "######################"
		print schedule
		db.session.add(schedule)
		db.session.commit()

		schedule_query = Schedule.query.filter(Schedule.park_id == park_id, Schedule.start_time == start_time).count()-1


		if schedule_query is None:
			less_start_time = start_time + timedelta(hours = n)
			add_end_time = end_time - timedelta (hours = n)
			suggestion_query = Schedule.query.filter(Schedule.park_id == park_id, Schedule.start_time == less_start_time).count()
			n+=1
			return jsonify(suggestion_query)

		return jsonify(schedule_query)

	else:

		flash("Try another time slot")
		return "reschedule"

	


@app.route('/logout')
def logout():
	"""Log out the user"""
	session.pop("user_id",None)
	flash("You've logged out!")
	return redirect('/')



@app.route('/parks')
def parks_list():
	"""Displays list of parks in San Francisco"""
	zipcode_list = db.session.query(Park.zipcode).all();
	zipcode_temp = [zip[0] for zip in zipcode_list]
	zip_uniq =set(zipcode_temp)
	zipcodes = list(zip_uniq)
	parks = Park.query.options(db.joinedload('scores')).order_by(Park.zipcode).all()

	return render_template("parks_list.html", parks=parks,zipcodes=zipcodes)

@app.route('/parks/<int:park_id>')
def report_info(park_id):
	"""Show parks with ratings and add ratings if user has logged in"""
	park = Park.query.get(park_id)

	return render_template('park_info.html', park=park)

@app.route('/parks/<int:park_id>/edit')
def add_ratings(park_id):
	"""Add ratings if user has logged in"""
	clean_score = int(request.args.get("cleanscore"))
	equip_score = int(request.args.get("equipscore"))
	maintain_score = int(request.args.get("maintainscore"))
	total_score = (clean_score + equip_score + maintain_score)/ float(3)

	rating_score = Rating.query.filter(Rating.park_id == park_id).first()
	# try except 

	if not rating_score:
		rate = Rating(park_id = park_id, rating = total_score,reviews = 1)
		db.session.add(rate)

	else:
		temp = rating_score.reviews
		temp_count = rating_score.reviews+1
		rating_score.reviews = rating_score.reviews+1
		rating_score.rating = ((rating_score.rating*temp)+total_score)/float(temp_count)
		rating_score.rating = "{0:.1f}".format(rating_score.rating)
		print "!!!!!!!!!!!!!!!"
		print rating_score.rating
		rate = Rating(park_id = rating_score.park_id, rating = rating_score.rating, reviews = rating_score.reviews)
		db.session.add(rate)
	db.session.commit()
	flash("Thanks for feedback!!!")

	return redirect("/parks")



@app.route('/locatepark')
def locate_park():
	""" Locate a park when user types in a zip code """
	zipcode_list = []
	zipcode = int(request.args.get("zipcode"))
	locate_park = Park.query.filter(Park.zipcode == zipcode).all()
	if not locate_park:
		# import pdb; pdb.set_trace()
		flash('park not found in zipcode')
		n=1;
		while(n<=3):
			zip_less = zipcode -n;
			zip_add = zipcode+n;
			locate_1 = Park.query.filter(Park.zipcode == zip_less).all()
			if locate_1:
				zipcode_list.append(locate_1)
			locate_2= Park.query.filter(Park.zipcode == zip_add).all()
			if locate_2:
				zipcode_list.append(locate_2)
			n+=1
		print zipcode_list
		if zipcode_list:
			# session["zipcode_list"] = zipcode_list
			return render_template("locate_park.html",zipcode_list=zipcode_list,locatepark=None)
		else:
			flash(" park not found in neighbourhood. Try looking list of parks")
			return redirect("/")
	if locate_park:
		# import pdb; pdb.set_trace()
		# session["locate_park"] = locate_park
		return render_template("locate_park.html",locatepark=locate_park)


# app.route('/locatepark.json')
# def latlng_map():
# 	""" Having Multiple markers of the park list found in zipcode"""

# 	all_latlng = []
# 	if session["locate_park"]:
# 		for location in locate_park:
# 			latlng = {
# 			"lat"  : location.latitude,
# 			"lng"  : location.longitude,
# 			"name": location.parkname 
# 			}
# 			all_latlng.append(latlng)
# 	if session["zipcode_list"]:
# 		for location in zipcode_list:
# 			latlng = {
# 			"lat"  : location.latitude,
# 			"lng"  : location.longitude,
# 			"name": location.parkname 
# 			}
# 			all_latlng.append(latlng)
# 	return jsonify({'coordinates' : all_latlng})
















if __name__ == "__main__":

	# Set debug true so debug tool bar extension
	app.debug = True
	# templates are not cached in debug mode

	app.jinja_env.auto_reload = app.debug

	connect_to_db(app)
	# Use the DebugToolbar
	DebugToolbarExtension(app)
	app.run(port=5000, host='0.0.0.0')


