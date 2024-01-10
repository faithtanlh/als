CREATE TABLE LibMembers (
	membershipID	VARCHAR(8)		NOT NULL,
    fName			VARCHAR(50)		NOT NULL,
    lName			VARCHAR(50),
    faculty			VARCHAR(20),
    phoneNo			VARCHAR(15),
    eMail			VARCHAR(320)	NOT NULL,
    PRIMARY KEY (membershipID),
	UNIQUE (eMail));
CREATE TABLE Books (
	accessionNo		VARCHAR(5)		NOT NULL,
    title			VARCHAR(100)	NOT NULL,
    author1			VARCHAR(100),
    author2			VARCHAR(100),
    author3			VARCHAR(100),
    ISBN 			VARCHAR(13),
    publisher		VARCHAR(100),
    publicationYear	VARCHAR(4),
    PRIMARY KEY (accessionNo));
CREATE TABLE Reservations (
	reservationDate	DATE			NOT NULL,
    membershipID 	VARCHAR(8) 		NOT NULL,
    accessionNo		VARCHAR(5)		NOT NULL,
    PRIMARY KEY (membershipID, accessionNo),
    FOREIGN KEY (membershipID)	REFERENCES LibMembers(membershipID) 	ON DELETE NO ACTION
																	ON UPDATE CASCADE,
	FOREIGN KEY (accessionNo)	REFERENCES Books(accessionNo)	ON DELETE NO ACTION
																ON UPDATE CASCADE);
CREATE TABLE Loans (
	loanStart		DATE		NOT NULL,
    loanDue 		DATE		AS (date_add(loanStart, INTERVAL 14 DAY)),
    loanReturn		DATE		DEFAULT NULL,
    membershipID	VARCHAR(8)		NOT NULL,
    accessionNo 	VARCHAR(5)		NOT NULL,
    PRIMARY KEY (loanStart, membershipID, accessionNo),
    FOREIGN KEY (membershipID)	REFERENCES LibMembers(membershipID)	ON DELETE CASCADE
																	ON UPDATE CASCADE,
	FOREIGN KEY (accessionNo)	REFERENCES Books(accessionNo)	ON DELETE CASCADE
																ON UPDATE CASCADE);
CREATE TABLE Fines (
	paymentDate		DATE,
    paymentAmt		DECIMAL			DEFAULT 0,
    membershipID	VARCHAR(8)		NOT NULL,
    PRIMARY KEY (membershipID),
    FOREIGN KEY (membershipID)	REFERENCES LibMembers(membershipID)	ON DELETE CASCADE
																	ON UPDATE CASCADE);
	
    