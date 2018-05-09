

from sqlalchemy import func
from model_db import User
from model_db import Park
from model_db import Rating
from model_db import Favorite

from model_db import connect_to_db,db
import csv

# from server import app


def load_parks():
	"""Load parks from park_data into database"""


	Park.query.delete()

	with open('park_Info.csv','rb') as csvfile:

		park_records = csv.DictReader(csvfile)
		

		for row in park_records:
			parkname=row['ParkName']
			manager = row['Manager']
			email = row['Email']
			phone = row['Phone']
			zipcode = row['zipcode']
			location = row['Location']


			park = Park(park_id=park_id, parkname=parkname,manager=manager,email=email,phone=phone,zipcode=zipcode,location=location)


			db.session.add(park)

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

	load_parks()
	set_val_user_id()

