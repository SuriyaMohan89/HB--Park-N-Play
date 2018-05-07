import csv

with open('parkfinal.csv','rb') as csvfile:

	park_records = csv.Dictreader(csvfile, delimiter=' ',quotechar=',')

	for record in park_records:
		print (row['ParkName'],row['PSAManager'],row['email'],row['zipcode'],row['Location'])





