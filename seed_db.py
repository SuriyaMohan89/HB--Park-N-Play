from model_db import User
from model_db import Park
from model_db import Rating
from model_db import Favorite

from model_db import connect_to_db,db
import csv


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

