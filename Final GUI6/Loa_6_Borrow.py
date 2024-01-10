from tkinter import *
from BT2102_ALS_functions import * 
import mysql.connector
from SQLpassword import get_password
from datetime import datetime

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()


class Loa_6_Borrow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "loabg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller
       
        #instruction
        mem_6_instruction = Label(self, text = "To Borrow a Book, Please Enter Information Below:", font=controller.title_font, bg="#b1b8c0")
        mem_6_instruction.place(relx=0.5, rely=0.2, anchor=CENTER)
        #mem_6_instruction.grid(row=1, column=1, sticky="W", pady=5)

        #labels
        mem_6_acc_lab = Label(self, text = "Accession number", font=controller.normal_font, bg="#b1b8c0")
        mem_6_acc_lab.place(relx=0.33, rely=0.4, anchor=CENTER)
        #mem_6_acc_lab.grid(row=3, column=0, sticky="E", padx=5, pady=10)
        mem_6_menID_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_6_menID_lab.place(relx=0.33, rely=0.6, anchor=CENTER)
        #mem_6_menID_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_6_acc_ent = Entry(self, width=30, font=controller.normal_font)
        mem_6_acc_ent.place(relx=0.66, rely=0.4, anchor=CENTER)
        #mem_6_acc_ent.grid(row=3, column=1, padx=5, pady=10)
        mem_6_memID_ent = Entry(self, width=30, font=controller.normal_font)
        mem_6_memID_ent.place(relx=0.66, rely=0.6, anchor=CENTER)
        #mem_6_memID_ent.grid(row=5, column=1, padx=5, pady=10)

        def checkBookExists(accession_no):
            mycursor.execute("SELECT accessionNo FROM Books WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def invalidAccessionNo(accession_no):
            if len(accession_no) > 5:
                return True
            return False

        def checkMemberExists(mem_id):
            mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def invalidMemID(mem_id):
            ref_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if mem_id == "":
                return False
            elif (len(mem_id) > 8) or(mem_id[0] not in ref_alphabets) or (mem_id[-1] not in ref_alphabets) or \
                (mem_id[1:-1].isdigit() == False):
                return True
            else:
                return False

        #button functions
        def confirm_popup():
            if invalidAccessionNo(mem_6_acc_ent.get()):
                global pop6
                pop6 = Toplevel(self)
                pop6.title("Error!")
                pop6.geometry("600x400")
                pop6.config(bg="#C53A5A")

                pop6_label1 = Label(pop6, text="Error!", font=controller.normal_font)
                pop6_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop6_label2 = Label(pop6, text= "Invalid accession number", font=controller.normal_font)      #backend determine which error msg
                pop6_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop6, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop6, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop6.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkBookExists(mem_6_acc_ent.get()):
                global pop4
                pop4 = Toplevel(self)
                pop4.title("Error!")
                pop4.geometry("600x400")
                pop4.config(bg="#C53A5A")

                pop4_label1 = Label(pop4, text="Error!", font=controller.normal_font)
                pop4_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop4_label2 = Label(pop4, text= "Book does not exist", font=controller.normal_font)      #backend determine which error msg
                pop4_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop4, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop4, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop4.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if invalidMemID(mem_6_memID_ent.get()):
                global pop7
                pop7 = Toplevel(self)
                pop7.title("Error!")
                pop7.geometry("600x400")
                pop7.config(bg="#C53A5A")

                pop7_label1 = Label(pop7, text="Error!", font=controller.normal_font)
                pop7_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop7_label2 = Label(pop7, text= "Invalid membership ID", font=controller.normal_font)      #backend determine which error msg
                pop7_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop7, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop7, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop7.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkMemberExists(mem_6_memID_ent.get()):
                global pop5
                pop5 = Toplevel(self)
                pop5.title("Error!")
                pop5.geometry("600x400")
                pop5.config(bg="#C53A5A")

                pop5_label1 = Label(pop5, text="Error!", font=controller.normal_font)
                pop5_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop5_label2 = Label(pop5, text= "Member does not exist", font=controller.normal_font)      #backend determine which error msg
                pop5_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop5, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop5, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop5.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return

            global pop1
            pop1 = Toplevel(self)
            pop1.title("Confirm loan details")
            pop1.geometry("600x400")
            pop1.config(bg="#3ac5a5")

            def get_accession_number():
                return mem_6_acc_ent.get()

            def get_title():
                acc_no = mem_6_acc_ent.get()
                mycursor.execute("SELECT title FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                return result

            def get_borrowdate():
                mycursor.execute("SELECT CAST(NOW() AS DATE)")
                borrow_date = str(mycursor.fetchone()[0])
                date_values = borrow_date.split("-")
                borrow_date = date_values[2] + "/" + date_values[1] + "/" + date_values[0]
                return borrow_date

            def get_memID():
                return mem_6_memID_ent.get()

            def get_memName():
                mem_id = mem_6_memID_ent.get()
                mycursor.execute("SELECT lName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                result = mycursor.fetchone()[0]
                if result != None:
                    mycursor.execute("SELECT concat(fName, ' ', lName) FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                else:
                    mycursor.execute("SELECT fName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                return final_result

            def get_dueDate():
                mycursor.execute("SELECT CAST(NOW() AS DATE)")
                borrow_date = mycursor.fetchone()[0]
                mycursor.execute("SELECT date_add(%s, INTERVAL 14 DAY)", (borrow_date,))
                due_date = str(mycursor.fetchone()[0])
                #due_date = str(borrow_date + datetime.timedelta(days = 14))
                date_values = due_date.split("-")
                due_date = date_values[2] + "/" + date_values[1] + "/" + date_values[0]
                return due_date

            pop1_label_main = Label(pop1, text="Confirm Loan Details To Be Correct", font=controller.normal_font)
            pop1_label_main.place(relx=0.5, rely=0.1, anchor=CENTER)

            pop1_label_accnum = Label(pop1, text= get_accession_number(), font=controller.normal_font)  ##quotation marks are to test
            pop1_label_accnum.place(relx=0.5, rely=0.2, anchor=CENTER)           

            pop1_label_title = Label(pop1, text= get_title(), font=controller.normal_font)
            pop1_label_title.place(relx=0.5, rely=0.3, anchor=CENTER)            

            pop1_label_borrowdate = Label(pop1, text= get_borrowdate(), font=controller.normal_font)
            pop1_label_borrowdate.place(relx=0.5, rely=0.4, anchor=CENTER)

            pop1_label_memID = Label(pop1, text= get_memID(), font=controller.normal_font)
            pop1_label_memID.place(relx=0.5, rely=0.5, anchor=CENTER)

            pop1_label_memName = Label(pop1, text= get_memName(), font=controller.normal_font)
            pop1_label_memName.place(relx=0.5, rely=0.6, anchor=CENTER)

            pop1_label_dueDate = Label(pop1, text= get_dueDate(), font=controller.normal_font)
            pop1_label_dueDate.place(relx=0.5, rely=0.7, anchor=CENTER)

            borrow_frame = Frame(pop1, bg="#3ac5a5")
            borrow_frame.place(anchor=CENTER)

            confirm = Button(pop1, text="Confirm Loan", font=controller.normal_font, command= lambda: [borrow_or_error(), pop1.destroy()])  ##withdraw or error
            confirm.place(relx=0.33, rely=0.85, anchor=CENTER)

            back = Button(pop1, text="Back to Loan function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop1.destroy()])
            back.place(relx=0.66, rely=0.85, anchor=CENTER)


        def checkHasFines(mem_id):
            mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if result[0][0] > 0:
                return True
            return False

        def getLoanCount(mem_id):
            mycursor.execute("SELECT COUNT(accessionNo) FROM Loans WHERE membershipID = %s \
                AND loanReturn IS NULL", (mem_id,))
            result = mycursor.fetchone()
            result = result[0]
            return result

        def checkBookBorrowed(accession_no):
            mycursor.execute("SELECT accessionNo FROM Loans WHERE accessionNo = %s AND \
                loanReturn IS NULL", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def getLoanDueDate(accession_no):
            mycursor.execute("SELECT loanDue FROM Loans WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchone()
            result = result[0]
            return result

        def checkReserved(accession_no):
            mycursor.execute("SELECT accessionNo FROM Reservations WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0:
                return False
            return True

        def checkBookReservedByMem(accession_no, mem_id):
            mycursor.execute("SELECT * FROM Reservations WHERE membershipID = %s AND accessionNo = %s", (mem_id, accession_no))
            result = mycursor.fetchall()
            if len(result) == 0:
                return False
            return True

        def get_error():
            err = ""
            if not checkBookExists(mem_6_acc_ent.get()) and not checkMemberExists(mem_6_memID_ent.get()):
                err += "\nBook and member both do not exist;"
            elif not checkBookExists(mem_6_acc_ent.get()):
                err += "\nBook does not exist;"
            elif not checkMemberExists(mem_6_memID_ent.get()):
                err += "\nMember does not exist;"
            if checkHasFines(mem_6_memID_ent.get()):
                err += "\nMember has outstanding fines;"
            if getLoanCount(mem_6_memID_ent.get()) == 2:
                err += "\nMember loan quota of 2 books exceeded;"
            if checkBookBorrowed(mem_6_acc_ent.get()):
                loanDueDate = str(getLoanDueDate(mem_6_acc_ent.get()))
                date_values = loanDueDate.split("-")
                loanDueDate = date_values[2] + "/" + date_values[1] + "/" + date_values[0]
                err += "\nBook currently on loan until: " + loanDueDate + ";"
            elif checkReserved(mem_6_acc_ent.get()) and (not checkBookReservedByMem(mem_6_acc_ent.get(), mem_6_memID_ent.get())): ##if the book is reserved by someone else
                err += "\nUnable to loan book as this book has already been reserved;"
            err = err[:-1]
            return err

        def borrow_book():
            if checkBookReservedByMem(mem_6_acc_ent.get(), mem_6_memID_ent.get()): ##if the book is reserved by self
                mycursor.execute("SELECT CAST(NOW() AS DATE)")
                borrow_date = mycursor.fetchone()[0]
                sqlborrow = "INSERT INTO Loans (loanStart, membershipID, accessionNo) VALUES \
                    (%s, %s, %s)"
                valborrow = (borrow_date, mem_6_memID_ent.get(), mem_6_acc_ent.get())
                mycursor.execute(sqlborrow, valborrow)
                mydb.commit()
                mycursor.execute("DELETE FROM Reservations WHERE membershipID = %s", (mem_6_memID_ent.get(),))
                mydb.commit()
                msg = "Reserved book is borrowed by member"
            else: ##book not reserved by anyone
                mycursor.execute("SELECT CAST(NOW() AS DATE)")
                borrow_date = mycursor.fetchone()[0]
                sqlborrow = "INSERT INTO Loans (loanStart, membershipID, accessionNo) VALUES \
                    (%s, %s, %s)"
                valborrow = (borrow_date, mem_6_memID_ent.get(), mem_6_acc_ent.get())
                mycursor.execute(sqlborrow, valborrow)
                mydb.commit()
                msg = "Book is borrowed by member"
            
            global pop3
            pop3 = Toplevel(self)
            pop3.title("Success!")
            pop3.geometry("600x400")
            pop3.config(bg="#3ac5a5")

            pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font)
            pop3_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
            pop3_label2 = Label(pop3, text=msg, font=controller.normal_font)
            pop3_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

            success_frame = Frame(pop3, bg="#3ac5a5")
            success_frame.place(anchor=CENTER)

            back = Button(pop3, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop3.destroy()])
            back.place(relx=0.5, rely=0.75, anchor=CENTER)
            ##insert code here to indicate book has been successfully borrowed

        def borrow_or_error():
            error_string = get_error()

            if error_string == "":   #backend check if book is on loan/exceeded loan quota/member has outstanding fines
                return borrow_book()            #backend borrow func
            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text= error_string, font=controller.normal_font)      #backend determine which error msg
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Borrow Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_6_Borrow"), pop2.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)




        #buttons
        mem_6_borrowButton = Button(self, text="Borrow book", padx=10, pady=10, font=controller.normal_font,
        bg="#b1b8c0", command=confirm_popup)
        mem_6_borrowButton.place(relx=0.25, rely=0.8)
        #mem_6_borrowButton.grid(row=80, column=2, padx=10, pady=10)

        mem_6_menuButton = Button(self, text="Back to Loans Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=lambda: controller.show_frame("LoanMenu"))
        mem_6_menuButton.place(relx=0.5, rely=0.8)
        #mem_6_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.8)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)


