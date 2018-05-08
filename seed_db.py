from model_db import User
from model_db import Park
from model_db import Rating
from model_db import Favorite

from model_db import connect_to_db,db


def load_parks():
	"""Load parks from park_data into database"""


	Park.query.delete()

	for row in open('park_data'):
		row = row.rstrip()
		parkname,manager,email,phone,location = row.split(',')

		park = Park(park_id=park_id, parkname=parkname,manager=manager,email=email,phone=phone,location=location)


		db.session.add(park)

	db.session.commit() 

