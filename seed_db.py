

from sqlalchemy import func
from model_db import User
from model_db import Park
from model_db import Rating
from model_db import Favorite
from model_db import Schedule
from model_db import connect_to_db,db
from faker import Faker
from random import randint
from datetime import date,time,datetime,timedelta
import csv


from server import app


# def load_users():
# 	"""Load users to the databse"""

# 	User.query.delete()
# 	print 'users deleted'

# 	user = User('username','email','password','zipcode')
# 	db.session.add(user)
# 	db.session.commit()


def load_parks():
	"""Load parks from park_data into database"""


	Park.query.delete()

	with open('park_Info.csv','rb') as csvfile:

		park_records = csv.reader(csvfile)
		

		for row in park_records:
			parkname,manager,email,phone,zipcode,address,latitude,longitude = row
			park = Park(parkname=parkname,manager=manager,email=email,phone=phone,zipcode=zipcode,location=address,latitude = latitude,longitude = longitude)


			db.session.add(park)

	db.session.commit() 


# def load_ratings():
# 	"""Load ratings into database"""
# 	Rating.query.delete()

# 	rating= Rating(park_id = park_id,rating= rating,reviews=reviews)
# 	db.session.add(rating)
# 	db.session.commit() 


# def load_schedule():
# 	"""Load scheduled date and time of an user for a park into database"""
# 	Rating.query.delete()

# 	schedule= Schedule(user_id=user_id,park_id = park_id,date= date,time=time)
# 	db.session.add()
# 	db.session.commit() 


def seed_user_datas(fake):
    """ Seed fake datas in database"""


    for i in range(30):
        user = User(username=fake.user_name(), email = fake.email(), password = 'Test123$', zipcode = fake.zipcode())
    #     db.session.add(user)
    # db.session.commit()

    # for i in range(100):

    	# start_temp = fake.future_datetime(end_date="+30d", tzinfo=None)
     #    start_time = start_temp.replace(minute=0,second=0)
     #    end_time = start_time + timedelta(hours=3)
     #    sche = Schedule(user_id = randint(1,30), park_id = randint(1,100),start_time = start_time, end_time = end_time) 
     #    print "@@@@@@@@@@@@@@@@@"
        db.session.add(user)
    db.session.commit()
def seed_schedule_datas(fake):

    for i in range(100):

		start_temp = fake.future_datetime(end_date="+30d", tzinfo=None)
		start_time = start_temp.replace(minute=0, second=0)
		end_time = start_time + timedelta(hours=3)
		sche = Schedule(user_id = randint(1,30), park_id = randint(1,100),start_time = start_time, end_time = end_time) 
		print sche
		db.session.add(sche)
    db.session.commit()




def set_val_user_id():
	"""Set value for the next user_id after seeding database"""

	#Get the Max user_id in the database
	result = db.session.query(func.max(User.user_id)).one()
	max_id = int(result[0])

	#Set the value for the next user_id to be max_id+1
	query = "SELECT setval('users_user_id_seq', :new_id)"
	db.session.execute(query,{'new_id': max_id + 1})
	db.session.commit()


if __name__ == '__main__':

	connect_to_db(app) 

	# Create table if table haven't been created
	db.create_all()
	fake = Faker()
	seed_user_datas(fake)
	seed_schedule_datas(fake)
	load_parks()
	# load_ratings()
	# load_schedule()
	# set_val_user_id()

