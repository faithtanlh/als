import mysql.connector

##Insert SQL password within the quotation marks below
my_password = ""

mydb = mysql.connector.connect(
	host = "localhost", 
	user = "root", 
	passwd = my_password, 
	database = "libals")

mycursor = mydb.cursor()

##Load LibBooks data (50 books) into database 

with open('LibBooks.txt') as f:
	lines = f.readlines()[1:]

for line in lines:
	args = line.split("/")
	for i in range(len(args)):
		if args[i] == "":
			args[i] = None;

	accession_number = args[0]
	book_title = args[1]
	author_1 = args[2]
	author_2 = args[3]
	author_3 = args[4]
	isbn = args[5]
	publisher = args[6]
	year = args[7]

	sql = "INSERT INTO Books (accessionNo, title, author1, author2, author3, ISBN, publisher, publicationYear) VALUES \
		(%s, %s, %s, %s, %s, %s, %s, %s)"
	val = (accession_number, book_title, author_1, author_2, author_3, isbn, publisher, year)
	mycursor.execute(sql, val)

mydb.commit()

mycursor.close()

##Load LibMems data (9 members) into database

mycursor = mydb.cursor()

with open('LibMems.txt') as f:
	lines = f.readlines()[1:]

for line in lines:
	args = line.split(",")
	for i in range(len(args)):
		if args[i] == "":
			args[i] = None

	membership_id = args[0]
	name = args[1].split(" ")
	fname = name[0]
	if len(name) > 1:
		lname = name[1]
	else:
		lname = None
	faculty = args[2]
	phone_num = args[3]
	email = args[4]

	sql = "INSERT INTO LibMembers (membershipID, fName, lName, faculty, phoneNo, eMail) VALUES \
		(%s, %s, %s, %s, %s, %s)"
	val = (membership_id, fname, lname, faculty, phone_num, email)
	mycursor.execute(sql, val)
	
	sql = "INSERT INTO Fines (paymentDate, membershipID) VALUES \
		(%s, %s)"
	val = (None, membership_id)
	mycursor.execute(sql, val)

mydb.commit()

mycursor.close()
mydb.close()
