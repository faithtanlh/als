from tkinter import *
from BT2102_ALS_functions import * 
import mysql.connector
from datetime import datetime
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()

class Res_8_MakeRes(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "resbg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.controller = controller
       
        #instruction 
        mem_8_instruction = Label(self, text = "To Reserve a Book, Please Enter Information Below:", font=controller.title_font, bg="#b1b8c0")
        #mem_8_instruction.grid(row=1, column=1, sticky="W", pady=5)
        mem_8_instruction.place(relx = 0.5, rely = 0.15, anchor = CENTER)

        #labels
        mem_8_acc_lab = Label(self, text = "Accession number", font=controller.normal_font, bg="#b1b8c0")
        mem_8_acc_lab.place(relx = 0.33, rely = 0.3, anchor = CENTER)
        #mem_8_acc_lab.grid(row=3, column=0, sticky="E", padx=5, pady=10)

        mem_8_memID_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_8_memID_lab.place(relx = 0.33, rely = 0.5, anchor = CENTER)
        #mem_8_menID_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        mem_8_reserveDate_lab = Label(self, text = "Reserve Date", font=controller.normal_font, bg="#b1b8c0")
        mem_8_reserveDate_lab.place(relx = 0.33, rely = 0.7, anchor = CENTER)
        #mem_8_reserveDate_lab.grid(row=7, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_8_acc_ent = Entry(self, width=30, font=controller.normal_font)
        mem_8_acc_ent.place(relx = 0.66, rely = 0.3, anchor = CENTER)
        #mem_8_acc_ent.grid(row=3, column=1, padx=5, pady=10)

        mem_8_memID_ent = Entry(self, width=30, font=controller.normal_font)
        mem_8_memID_ent.place(relx = 0.66, rely = 0.5, anchor = CENTER)
        #mem_8_memID_ent.grid(row=5, column=1, padx=5, pady=10)

        mem_8_reserveDate_ent = Entry(self, width=30, font=controller.normal_font)
        mem_8_reserveDate_ent.place(relx = 0.66, rely = 0.7, anchor = CENTER)
        #mem_8_reserveDate_ent.grid(row=7, column=1, padx=5, pady=10)

        def checkMemberExists(mem_id):
            mycursor.execute("SELECT membershipID FROM LibMembers WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

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

        def invalidMemID(mem_id):
            ref_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if mem_id == "":
                return False
            elif (len(mem_id) > 8) or(mem_id[0] not in ref_alphabets) or (mem_id[-1] not in ref_alphabets) or \
                (mem_id[1:-1].isdigit() == False):
                return True
            else:
                return False

        def checkDateFormat(date_string):
            if len(date_string) != 10:
                return False
            if date_string[2] != "/" or date_string[5] != "/":
                return False
            return date_string[:2].isdigit() and date_string[3:5].isdigit() and date_string[6:].isdigit()

        #button functions
        def confirm_popup():
            if invalidAccessionNo(mem_8_acc_ent.get()):
                global pop5
                pop5 = Toplevel(self)
                pop5.title("Error!")
                pop5.geometry("600x400")
                pop5.config(bg="#C53A5A")

                pop5_label1 = Label(pop5, text="Error!", font=controller.normal_font)
                pop5_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop5_label2 = Label(pop5, text= "Invalid accession number", font=controller.normal_font)      #backend determine which error msg
                pop5_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop5, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop5, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop5.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkBookExists(mem_8_acc_ent.get()):
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

                back = Button(pop4, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop4.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if invalidMemID(mem_8_memID_ent.get()):
                global pop6
                pop6 = Toplevel(self)
                pop6.title("Error!")
                pop6.geometry("600x400")
                pop6.config(bg="#C53A5A")

                pop6_label1 = Label(pop6, text="Error!", font=controller.normal_font)
                pop6_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop6_label2 = Label(pop6, text= "Invalid membership ID", font=controller.normal_font)      #backend determine which error msg
                pop6_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop6, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop6, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop6.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkMemberExists(mem_8_memID_ent.get()):
                global pop7
                pop7 = Toplevel(self)
                pop7.title("Error!")
                pop7.geometry("600x400")
                pop7.config(bg="#C53A5A")

                pop7_label1 = Label(pop7, text="Error!", font=controller.normal_font)
                pop7_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop7_label2 = Label(pop7, text= "Member does not exist", font=controller.normal_font)      #backend determine which error msg
                pop7_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop7, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop7, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop7.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if not checkDateFormat(mem_8_reserveDate_ent.get()):
                global pop8
                pop8 = Toplevel(self)
                pop8.title("Error!")
                pop8.geometry("600x400")
                pop8.config(bg="#C53A5A")

                pop8_label1 = Label(pop8, text="Error!", font=controller.normal_font)
                pop8_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop8_label2 = Label(pop8, text= "Invalid date format", font=controller.normal_font)      #backend determine which error msg
                pop8_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop8, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop8, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop8.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return

            global pop1
            pop1 = Toplevel(self)
            pop1.title("Confirm Reservation details")
            pop1.geometry("600x400")
            pop1.config(bg="#3ac5a5")

            def get_accession_number():
                return mem_8_acc_ent.get()

            def get_title():
                acc_no = mem_8_acc_ent.get()
                mycursor.execute("SELECT title FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                return result
            
            def get_memID():
                return mem_8_memID_ent.get()

            def get_memName():
                mem_id = mem_8_memID_ent.get()
                mycursor.execute("SELECT lName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                result = mycursor.fetchone()[0]
                if result != None:
                    mycursor.execute("SELECT concat(fName, ' ', lName) FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                else:
                    mycursor.execute("SELECT fName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                return final_result

            def get_reserveDate():
                return mem_8_reserveDate_ent.get()

            pop1_label_main = Label(pop1, text="Confirm Reservation Details To Be Correct", font=controller.normal_font)
            pop1_label_main.place(relx=0.5, rely=0.15, anchor=CENTER)

            pop1_label_accnum = Label(pop1, text= get_accession_number(), font=controller.normal_font)  ##quotation marks are to test
            pop1_label_accnum.place(relx=0.5, rely=0.3, anchor=CENTER)
            pop1_label_title = Label(pop1, text= get_title(), font=controller.normal_font)
            pop1_label_title.place(relx=0.5, rely=0.4, anchor=CENTER)
            pop1_label_memID = Label(pop1, text= get_memID(), font=controller.normal_font)
            pop1_label_memID.place(relx=0.5, rely=0.5, anchor=CENTER)
            pop1_label_memName = Label(pop1, text= get_memName(), font=controller.normal_font)
            pop1_label_memName.place(relx=0.5, rely=0.6, anchor=CENTER)
            pop1_label_reserveDate = Label(pop1, text= get_reserveDate(), font=controller.normal_font)
            pop1_label_reserveDate.place(relx=0.5, rely=0.7, anchor=CENTER)

            reserve_frame = Frame(pop1, bg="#3ac5a5")
            reserve_frame.place(anchor=CENTER)

            confirm = Button(pop1, text="Confirm Reservation", font=controller.normal_font, command=lambda: [reserve_or_error(), pop1.destroy()]) 
            confirm.place(relx=0.33, rely=0.85, anchor=CENTER)

            back = Button(pop1, text="Back to Reserve function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop1.destroy()])
            back.place(relx=0.66, rely=0.85, anchor=CENTER)


        def checkReserved(accession_no):
            mycursor.execute("SELECT accessionNo FROM Reservations WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0:
                return False
            return True

        def checkHasFines(mem_id):
            mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if result[0][0] > 0:
                return True
            return False

        def reserveLimitExceeded(mem_id):
            mycursor.execute("SELECT accessionNo FROM Reservations WHERE membershipID = %s", (mem_id,))
            result = mycursor.fetchall()
            if len(result) >= 2: 
                return True
            return False

        def checkBookBorrowed(accession_no):
            mycursor.execute("SELECT accessionNo FROM Loans WHERE accessionNo = %s AND \
                loanReturn IS NULL", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def get_error():
            err = ""
            if (mem_8_acc_ent.get() == "") or (mem_8_memID_ent.get() == ""):
                err += "\nMissing mandatory fields (Accession number, membership ID);"
            if not checkMemberExists(mem_8_memID_ent.get()):
                err += "\nMember does not exist;"
            if not checkBookExists(mem_8_acc_ent.get()):
                err += "\nBook cannot be found;"
            if checkReserved(mem_8_acc_ent.get()):
                err += "\nBook is already being reserved;"
            if checkHasFines(mem_8_memID_ent.get()):
                err += "\nMember currently has outstanding fines and cannot borrow books;"
            if reserveLimitExceeded(mem_8_memID_ent.get()):
                err += "\nMaximum reserve limit of 2 books reached;"
            if not checkBookBorrowed(mem_8_acc_ent.get()):
                err += "\nBook is currently available for loan;"
            err = err[:-1]
            return err

        def convert_to_date(date_string):
            dto = datetime.strptime(date_string, '%m/%d/%Y').date()
            return dto

        def reserve_book():
            reserve_date = convert_to_date(mem_8_reserveDate_ent.get())
            sql = "INSERT INTO Reservations (reservationDate, membershipID, accessionNo) VALUES \
                (%s, %s, %s)"
            val = (reserve_date, mem_8_memID_ent.get(), mem_8_acc_ent.get())
            mycursor.execute(sql, val)
            mydb.commit()

            global pop3
            pop3 = Toplevel(self)
            pop3.title("Success!")
            pop3.geometry("600x400")
            pop3.config(bg="#3ac5a5")

            pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font)
            pop3_label1.place(relx=0.5, rely=0.25,anchor=CENTER)
            pop3_label2 = Label(pop3, text="Book has been successfully reserved.", font=controller.normal_font)
            pop3_label2.place(relx=0.5, rely=0.5,anchor=CENTER)

            success_frame = Frame(pop3, bg="#3ac5a5")
            success_frame.place(anchor=CENTER)

            back = Button(pop3, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop3.destroy()])
            back.place(relx=0.5, rely=0.75,anchor=CENTER)
            ##insert pop up code here

        def reserve_or_error():
            error_string = get_error()

            if error_string == "":   #backend check if member alrd has 2 books reserved or if member has outstanding fines
                return reserve_book()            #backend reserve func
            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25,anchor=CENTER)
                pop2_label2 = Label(pop2, text= error_string, font=controller.normal_font)      #backend determine which error msg
                pop2_label2.place(relx=0.5, rely=0.5,anchor=CENTER)

                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Reserve Function", font=controller.normal_font, command=lambda: [controller.show_frame("Res_8_MakeRes"), pop2.destroy()])
                back.place(relx=0.5, rely=0.75,anchor=CENTER)

        #buttons
        mem_8_reserveButton = Button(self, text="Reserve book", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=confirm_popup)
        mem_8_reserveButton.place(relx = 0.25, rely = 0.85, anchor = CENTER)
        #mem_8_reserveButton.grid(row=80, column=2, padx=10, pady=10)

        mem_8_menuButton = Button(self, text="Back to Reservation Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=lambda: controller.show_frame("ReservationMenu"))
        mem_8_menuButton.place(relx = 0.5, rely = 0.85, anchor = CENTER)
        #mem_8_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx = 0.75, rely = 0.85, anchor = CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)


