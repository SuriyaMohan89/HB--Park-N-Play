import csv

with open('parkfinal_git_1.csv','rb') as csvfile:

	park_records = csv.DictReader(csvfile, delimiter=' ',quotechar=',')

	for row in park_records:
		# print row
		print row['ParkName,PSAManager,email,phone,zipcode,Location']






