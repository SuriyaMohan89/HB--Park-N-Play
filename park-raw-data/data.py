import csv

with open('park_Info.csv','rb') as csvfile:

	park_records = csv.DictReader(csvfile)
	details =[]

	for row in park_records:
		print row['Location']




