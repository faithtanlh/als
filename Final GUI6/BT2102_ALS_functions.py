import mysql.connector
from mysql.connector import errorcode
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()

#getBooksOnLoan function
def getBooksOnLoan():
    mycursor.execute("SELECT t1.* FROM Books AS t1 INNER JOIN Loans AS \
        t2 ON t1.accessionNo = t2.accessionNo WHERE t2.loanReturn IS NULL")
    result = mycursor.fetchall()
    return result

#getReservedBooks function
def getReservedBooks():
    mycursor.execute("SELECT T3.accessionNo, T1.title, T3.membershipID, concat(fName, ' ', lName) name \
        FROM (Books as T1 INNER JOIN Reservations as T3 ON T1.accessionNo = T3.accessionNo) \
        INNER JOIN LibMembers as T2 ON T2.membershipID = T3.membershipID ORDER BY accessionNo;")
    result = mycursor.fetchall()
    return result

#getMembersWithFine function
def getMembersWithFine():
    mycursor.execute("SELECT t1.membershipID, concat(fName, ' ', lName) name, faculty, phoneNo, eMail \
        FROM LibMembers AS t1 INNER JOIN Fines AS t2 ON t1.membershipID = t2.membershipID;")
    result = mycursor.fetchall()
    return result

#getBooksLoanedByMemID function
def getBooksLoanedByMemID(mem_id):
    mycursor.execute("SELECT t1.* FROM Books AS t1 INNER JOIN Loans AS t2 ON t1.accessionNo = \
        t2.accessionNo WHERE t2.membershipID = mem_id;")
    result = mycursor.fetchall()
    return result

#createMember function(s)
class InvalidMemID(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

# Exceptions for PhoneNo
class InvalidPhoneNo(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def memID_used(mem_id):
    mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchall()
    if len(result) == 0: 
        return False
    return True

def email_used(email):
    mycursor.execute("SELECT eMail FROM LibMembers WHERE eMail = %s", (email,))
    result = mycursor.fetchall()
    if len(result) == 0: 
        return False
    return True

def checkMemID(mem_id):
    ref_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if mem_id == "":
        return mem_id
    elif (len(mem_id) > 8) or(mem_id[0] not in ref_alphabets) or (mem_id[-1] not in ref_alphabets) or \
        (mem_id[1:-1].isdigit() == False):
        raise InvalidMemID("Invalid Membership ID entered")
    else:
        return mem_id

def checkPhoneNo(phoneNo):
    if phoneNo == "":
        return phoneNo
    if (len(phoneNo) != 8) or (not phoneNo.isdigit()):
        raise InvalidPhoneNo("Invalid phone number entered")
    else:
        return phoneNo

def createMember(mem_id, fName, lName, faculty, phoneNo, email):
    faculty = faculty.capitalize()
    try:
        mem_id = checkMemID(mem_id)
        phoneNo = checkPhoneNo(phoneNo)
        if mem_id == "":
            mem_id = None
        if fName == "":
            fName = None
        if lName == "":
            lName = None
        if faculty == "":
            faculty = None
        if phoneNo == "":
            phoneNo = None
        if email == "":
            email = None
        sql = "INSERT INTO LibMembers (membershipID, fName, lName, faculty, phoneNo, eMail) VALUES \
            (%s, %s, %s, %s, %s, %s)"
        val = (mem_id, fName, lName, faculty, phoneNo, email)
        mycursor.execute(sql, val)
        sql = "INSERT INTO Fines (paymentDate, paymentAmt, membershipID) VALUES (%s, %s, %s)"
        val = (None, 0, mem_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err1:
        if err1.errno == 1048:
            msg = "Missing mandatory fields (Membership ID, first name, email)"
            print(msg)
        if err1.errno == 1062:
            if memID_used(mem_id) and email_used(email):
                msg = "Member already exists: Membership ID and email are currently in use"
                print(msg)
            elif memID_used(mem_id):
                msg = "Membership ID is currently in use"
                print(msg)
            else:
                msg = "Email is currently in use"
                print(msg)
    except InvalidMemID as err2:
        print(err2)
    except InvalidPhoneNo as err3:
        print(err3)
    else:
        print("Membership account created successfully")

##Test cases
#createMember('A101B', 'CHLOE', 'ONG', 'COMPUTING', '12345678', 'E0773170@U.NUS.EDU') 
#createMember('a101a', 'CHLOE', 'ONG', 'COMPUTING', '12345678', 'E0773170@U.NUS.EDU')
#createMember('12345', 'CHLOE', 'ONG', 'COMPUTING', '12345678', 'E0773170@U.NUS.EDU')
#createMember('A1010A', 'CHLOE', 'ONG', 'COMPUTING', '12345678', 'E0773170@U.NUS.EDU')

#checkMemberExists function
def checkMemberExists(mem_id):
    mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchall()
    if len(result) == 0: 
        return False
    return True

#deleteMember function
def deleteMember(mem_id):
    error_string = ""   
    if not checkMemberExists(mem_id): 
        return "No such member exists"
    else:
        mycursor.execute("SELECT membershipID FROM Loans WHERE membershipID = %s AND loanReturn IS NULL", (mem_id,))
        result = mycursor.fetchall()
        if len(result) != 0:
            error_string += "Member has yet to return loaned books;"

        mycursor.execute("SELECT membershipID FROM Reservations WHERE membershipID = %s", (mem_id,))
        result = mycursor.fetchall()
        if len(result) != 0:
            error_string += "Member still has some books reserved;"
        
        mycursor.execute("SELECT membershipID FROM Fines WHERE membershipID = %s AND paymentAmt != 0", (mem_id,))
        result = mycursor.fetchall()
        if len(result) != 0:
            error_string += "Member has outstanding fines;"
    
    if len(error_string) == 0:
        mycursor.execute("DELETE FROM LibMembers WHERE membershipID = %s", (mem_id,))
        mydb.commit()
        print("Membership account successfully deleted")
    else:
        print(error_string[:-1])
        
##Test Cases      
#deleteMember('A201B')

#updateMember function(s) (Remember to check if member exists using checkMemberExists function prior to running this!)
def updateName(mem_id, fName, lName):
    try:
        if fName == "":
            fName = None
        if lName == "":
            lName = None
        sql = "UPDATE LibMembers SET fName = %s, lName = %s WHERE membershipID = %s"
        val = (fName, lName, mem_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == 1048:
            msg = "Missing mandatory field (First name)"
            print(msg)
    else:
        print("Updated member name")

def updateFaculty(mem_id, faculty):
    if faculty == "":
        faculty = None
    sql = "UPDATE LibMembers SET faculty = %s WHERE membershipID = %s"
    val = (faculty, mem_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Updated member faculty")

def updatePhoneNo(mem_id, phoneNo):
    try:
        phoneNo = checkPhoneNo(phoneNo)
        if phoneNo == "":
            phoneNo = None
        sql = "UPDATE LibMembers SET phoneNo = %s WHERE membershipID = %s"
        val = (phoneNo, mem_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except InvalidPhoneNo as err:
        print(err)
    else:
        print("Updated member phone number")

def updateEmail(mem_id, email):
    try:
        if email == "":
            email = None
        sql = "UPDATE LibMembers SET eMail = %s WHERE membershipID = %s"
        val = (email, mem_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == 1048:
            msg = "Missing mandatory field (Email)"
            print(msg)
        if err.errno == 1062:
            msg = "Email is currently in use"
            print(msg)
    else:
        print("Updated member email")

#checkBookExists function
def checkBookExists(accession_no):
    mycursor.execute("SELECT accessionNo FROM Books WHERE accessionNo = %s", (accession_no,))
    result = mycursor.fetchall()
    if len(result) == 0: 
        return False
    return True

#reserveLimitExceeded function
def reserveLimitExceeded(mem_id):
    mycursor.execute("SELECT accessionNo FROM Reservations WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchall()
    if len(result) >= 2: 
        return True
    return False

#getLoanCount function
def getLoanCount(mem_id):
    mycursor.execute("SELECT COUNT(accessionNo) FROM Loans WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchone()
    result = result[0]
    return result

#getLoanDueDate function
def getLoanDueDate(accession_no):
    mycursor.execute("SELECT loanDue FROM Loans WHERE accessionNo = %s", (accession_no,))
    result = mycursor.fetchone()
    result = result[0]
    return result

#checkBookBorrowed function
def checkBookBorrowed(accession_no):
    mycursor.execute("SELECT accessionNo FROM Loans WHERE accessionNo = %s AND \
        loanReturn IS NULL", (accession_no,))
    result = mycursor.fetchall()
    if len(result) == 0: 
        return False
    return True

#checkHasFines function
def checkHasFines(mem_id):
    mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchall()
    if result[0][0] > 0:
        return True
    return False

#checkReserved function
def checkReserved(accession_no):
    mycursor.execute("SELECT accessionNo FROM Reservations WHERE accessionNo = %s", (accession_no,))
    result = mycursor.fetchall()
    if len(result) == 0:
        return False
    return True

#checkBookReservedByMem function
def checkBookReservedByMem(accession_no, mem_id):
    mycursor.execute("SELECT * FROM Reservations WHERE membershipID = %s AND accessionNo = %s", (mem_id, accession_no))
    result = mycursor.fetchall()
    if len(result) == 0:
        return False
    return True

#getMemReturningBook function (before updating)
def getMemReturningBook(accession_no):
    mycursor.execute("SELECT membershipID FROM Loans WHERE accessionNo = %s AND loanReturn IS NULL", (accession_no,))
    result = mycursor.fetchone()[0]
    return result

#acquireBook function
def acquireBook(accession_no, title, author1, author2, author3, isbn, publisher, publicationYear):
    if accession_no == "":
        accession_no = None
    if title == "":
        title = None
    if author1 == "":
        author1 = None
    if author2 == "":
        author2 = None
    if author3 == "":
        author3 = None
    if isbn == "":
        isbn = None
    if publisher == "":
        publisher = None
    if publicationYear == "":
        publicationYear = None
    
    try:
        sql = "INSERT INTO Books (accessionNo, title, author1, author2, author3, ISBN, publisher, publicationYear) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (accession_no, title, author1, author2, author3, isbn, publisher, publicationYear)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == 1048:
            msg = "Missing mandatory fields (accessionNo, title)"
            print(msg)
        if err.errno == 1062:
            if checkBookExists(accession_no):
                msg = "Book already exists: Book accession number is already in use"
                print(msg)
    else:
        print("Success! New book added in Library")

#Test cases
#print(acquireBook('', 'Brave New World', 'Aldous Huxley', '', '', '9790000000003', 'Harper Perrenial', '2006'))
#print(acquireBook('A03', '', 'Aldous Huxley', '', '', '9790000000003', 'Harper Perrenial', '2006'))
#print(acquireBook('', '', 'Aldous Huxley', '', '', '9790000000003', 'Harper Perrenial', '2006'))
#print(acquireBook('A30', 'Brave New World', 'Aldous Huxley', '', '', '9790000000003', 'Harper Perrenial', '2006'))
#print(acquireBook('A51', 'Brave New World', 'Aldous Huxley', '', '', '9790000000003', 'Harper Perrenial', '2006'))

#withdrawBook function
def withdrawBook(accession_no):
    if not checkBookExists(accession_no):
        print("Book does not exist")
        return
    if checkBookBorrowed(accession_no):
        print("Book is currently on loan")
        return
    if checkReserved(accession_no):
        print("Book is currently reserved")
        return
    
    mycursor.execute("DELETE FROM Books WHERE accessionNo = %s", (accession_no,))
    mydb.commit()
    print("Book withdrawn successfully")
    return 
    
#borrowBook function (need to consider if the book is reserved (can only loan to member who reserved))
def borrowBook(accession_no, mem_id):
    if not checkBookExists(accession_no) and not checkMemberExists(mem_id):
        print("Book and member both do not exist")
        return 
    if not checkBookExists(accession_no):
        print("Book does not exist")
        return 
    if not checkMemberExists(mem_id):
        print("Member does not exist")
        return 
    if checkHasFines(mem_id):
        print("Member has outstanding fines")
        return 
    if getLoanCount(mem_id) == 2:
        print("Member loan quota of 2 books exceeded")
        return 
    if checkBookBorrowed(accession_no):
        loanDueDate = str(getLoanDueDate(accession_no))
        date_values = loanDueDate.split("-")
        loanDueDate = date_values[2] + "/" + date_values[1] + "/" + date_values[0]
        print("Book currently on loan until: " + loanDueDate)
        return 
    if checkBookReservedByMem(accession_no, mem_id): ##if the book is reserved by self
        mycursor.execute("SELECT CAST(NOW() AS DATE)")
        borrow_date = mycursor.fetchone()[0]
        sqlborrow = "INSERT INTO Loans (loanStart, membershipID, accessionNo) VALUES \
            (%s, %s, %s)"
        valborrow = (borrow_date, mem_id, accession_no)
        mycursor.execute(sqlborrow, valborrow)
        mydb.commit()
        mycursor.execute("DELETE FROM Reservations WHERE membershipID = %s", (mem_id,))
        mydb.commit()
        print("Reserved book is borrowed by member")
    elif checkReserved(accession_no): ##if the book is reserved by someone else
        print("Unable to loan book as this book has already been reserved")
    else: ##if the book is not reserved by anyone
        mycursor.execute("SELECT CAST(NOW() AS DATE)")
        borrow_date = mycursor.fetchone()[0]
        sqlborrow = "INSERT INTO Loans (loanStart, membershipID, accessionNo) VALUES \
            (%s, %s, %s)"
        valborrow = (borrow_date, mem_id, accession_no)
        mycursor.execute(sqlborrow, valborrow)
        mydb.commit()
        print("Book is borrowed by member")
    
#returnBook function (need to consider if the book is past due date(incur fines))
def returnBook(accession_no):
    mycursor.execute("SELECT CAST(NOW() AS DATE)")
    return_date = mycursor.fetchone()[0]
    if not checkBookExists(accession_no):
        print("Book does not exist")
        return 
    if (return_date > getLoanDueDate(accession_no)):
        mycursor.execute("SELECT DATEDIFF(%s, %s)", (return_date, getLoanDueDate(accession_no)))
        dateDiff = mycursor.fetchone()[0]
        sql = "UPDATE Fines SET paymentAmt = %s WHERE membershipID = %s"
        val = (dateDiff, getMemReturningBook(accession_no))
        mycursor.execute(sql, val)
        mydb.commit()
        print("Book returned successfully but has incurred fines")
    else:
        print("Book returned successfully")

    mycursor.execute("UPDATE Loans SET loanReturn = %s WHERE accessionNo = %s AND \
        membershipID = %s", (return_date, accession_no, getMemReturningBook(accession_no)))
    mydb.commit()
    return 

#reserveBook function
def reserveBook(accession_no, mem_id):
    if (accession_no == "") or (mem_id == ""):
        print("Missing mandatory fields (Accession number, membership ID)")
        return
    if not checkMemberExists(mem_id):
        print("Member does not exist")
        return
    if not checkBookExists(accession_no):
        print("Book cannot be found")
        return
    if checkReserved(accession_no):
        print("Book is already being reserved")
        return
    if checkHasFines(mem_id):
        print("Member currently has outstanding fines and cannot borrow books")
        return 
    if reserveLimitExceeded(mem_id):
        print("Maximum reserve limit of 2 books reached")
        return
    if not checkBookBorrowed(accession_no):
        print("Book is currently available for loan")
        return
    try:
        mycursor.execute("SELECT CAST(NOW() AS DATE)")
        reserve_date = mycursor.fetchone()[0]
        sql = "INSERT INTO Reservations (reservationDate, membershipID, accessionNo) VALUES \
            (%s, %s, %s)"
        val = (reserve_date, mem_id, accession_no)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == 1452:
            if not checkMemberExists(mem_id):
                print("Member does not exist")
            if not checkBookExists(accession_no):
                print("Book cannot be found")
    else:
        print("Book has successfully been reserved for member")

#Test cases
#reserveBook('A05', 'A101A')

#cancelReservation function
def cancelReservation(accession_no, mem_id):
    if (accession_no == "") or (mem_id == ""):
        print("Missing mandatory fields (Accession number, membership ID)")
        return
    if not checkMemberExists(mem_id):
        print("Member does not exist")
        return
    if not checkBookExists(accession_no):
        print("Book cannot be found")
        return
    if not checkReserved(accession_no):
        print("Book is currently not reserved")
        return
    if not checkBookBorrowed(accession_no):
        print("Reservation cannot be cancelled as book is already available for loan")
        return
    try:
        sql = "DELETE FROM Reservations WHERE accessionNo = %s AND membershipID = %s"
        val = (accession_no, mem_id)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as err:
        if err.errno == 1452: ##Check if this error code is correct
            if not checkMemberExists(mem_id):
                print("Member does not exist")
            if not checkBookExists(accession_no):
                print("Book cannot be found")
    else:
        print("Reservation cancelled")

#cancelReservation("A36", "A101A")
#cancelReservation("A43", "A101A")

#isOneWord function
def isOneWord(word):
    return len(word.split(" ")) <= 1

#searchBook function
def searchBook(search_title, search_authors, search_isbn, search_publisher, search_year):
    if search_title == "" and search_authors == "" and search_isbn == "" and search_publisher == "" \
        and search_year == "":
        print("Search not specified")
        return
    if not(isOneWord(search_title) and isOneWord(search_authors) and isOneWord(search_isbn) and \
        isOneWord(search_publisher) and isOneWord(search_year)):
        print("Only one word is accepted for each search field")
        return
    if search_title == "":
        search_title = "%"
    else:
        search_title = "%" + search_title + "%"
    if search_authors == "":
        search_authors = "%"
    else:
        search_authors = "%" + search_authors + "%"
    if search_isbn == "":
        search_isbn = "%"
    else:
        search_isbn = "%" + search_isbn + "%"
    if search_publisher == "":
        search_publisher = "%"
    else:
        search_publisher = "%" + search_publisher + "%"
    if search_year == "":
        search_year = "%"
    else:
        search_year = "%" + search_year + "%"
    sql = "SELECT accessionNo, title, author1, author2, author3, ISBN, publisher, publicationYear \
        FROM Books WHERE title LIKE %s AND (author1 LIKE %s OR author2 LIKE %s OR author3 LIKE %s) \
        AND ISBN LIKE %s AND publisher LIKE %s AND publicationYear LIKE %s"
    val = (search_title, search_authors, search_authors, search_authors, search_isbn, search_publisher, search_year)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return result

#Test cases
#print(searchBook("", "", "", "", ""))
#print(searchBook("", "", "", "", "2021"))
#print(searchBook("", "", "", "Classics", ""))
#print(searchBook("", "", "9790000000001", "", ""))
#print(searchBook("", "Rand", "", "", ""))
#print(searchBook("1984", "", "", "", ""))

#payFine function
def payFine(payment_amt, mem_id):
    if not checkMemberExists(mem_id):
        print("Member does not exist")
        return

    mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_id,))
    result = mycursor.fetchone()[0]
    cumulative_amt = float(result)
    if cumulative_amt == 0:
        print("Member has no fines to pay")
        return
    elif cumulative_amt != payment_amt:
        print("Incorrect payment amount: exact payment is required")
        return
    
    mycursor.execute("SELECT CAST(NOW() AS DATE)")
    payment_date = mycursor.fetchone()[0]
    sql = "UPDATE Fines SET paymentDate = %s, paymentAmt = 0 WHERE membershipID = %s"
    val = (payment_date, mem_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Fines have been completely paid")

#Test cases
#payFine(0, 'A101B')
    

