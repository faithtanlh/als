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

mycursor = mydb.cursor(buffered=True)


class Loa_7_Return(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "loabg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller
       
        #instruction
        mem_7_instruction = Label(self, text = "To Return a Book, Please Enter Information Below:", font=controller.title_font, bg="#b1b8c0")
        mem_7_instruction.place(relx=0.5, rely=0.2, anchor=CENTER)
        #mem_7_instruction.grid(row=1, column=1, sticky="W", pady=5)

        #labels
        mem_7_acc_lab = Label(self, text = "Accession Number", font=controller.normal_font, bg="#b1b8c0")
        mem_7_acc_lab.place(relx=0.33, rely=0.4, anchor=CENTER)
        #mem_7_acc_lab.grid(row=3, column=0, sticky="E", padx=5, pady=10)

        mem_7_returnDate_lab = Label(self, text = "Return Date", font=controller.normal_font, bg="#b1b8c0")
        mem_7_returnDate_lab.place(relx=0.33, rely=0.6, anchor=CENTER)
        #mem_7_returnDate_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_7_acc_ent = Entry(self, width=30, font=controller.normal_font)
        mem_7_acc_ent.place(relx=0.66, rely=0.4, anchor=CENTER)
        #mem_7_acc_ent.grid(row=3, column=1, padx=5, pady=10)

        mem_7_returnDate_ent = Entry(self, width=30, font=controller.normal_font)
        mem_7_returnDate_ent.place(relx=0.66, rely=0.6, anchor=CENTER)
        #mem_7_returnDate_ent.grid(row=5, column=1, padx=5, pady=10)

        def checkBookExists(accession_no):
            mycursor.execute("SELECT accessionNo FROM Books WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            mycursor.close()
            if len(result) == 0: 
                return False
            return True

        def invalidAccessionNo(accession_no):
            if len(accession_no) > 5:
                return True
            return False

        def checkBookBorrowed(accession_no):
            mycursor = mydb.cursor()
            mycursor.execute("SELECT accessionNo FROM Loans WHERE accessionNo = %s AND \
                loanReturn IS NULL", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def checkDateFormat(date_string):
            if len(date_string) != 10:
                return False
            if date_string[2] != "/" or date_string[5] != "/":
                return False
            return date_string[:2].isdigit() and date_string[3:5].isdigit() and date_string[6:].isdigit()

        # def get_error():
        #     err = ""
        #     if not checkBookExists(mem_7_acc_ent.get()):
        #         err += "\nBook does not exist;"
        #     if not checkBookBorrowed(mem_7_acc_ent.get()):
        #         err += "\nBook is not borrowed;"
        #     if checkDateFormat(mem_7_returnDate_ent.get()):
        #         err += "\nInvalid date format;"
        #     err = err[:-1]
        #     return err

        def convert_to_date(date_string):
            dto = datetime.strptime(date_string, '%d/%m/%Y').date()
            return dto

        def getLoanDueDate(accession_no):
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("SELECT loanDue FROM Loans WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchone()
            result = result[0]
            return result

        def getMemReturningBook(accession_no):
            mycursor = mydb.cursor()
            mycursor.execute("SELECT membershipID FROM Loans WHERE accessionNo = %s AND loanReturn IS NULL", (accession_no,))
            result = mycursor.fetchone()[0]
            return result

        #button functions
        def confirm_popup():
            if invalidAccessionNo(mem_7_acc_ent.get()):
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

                back = Button(pop5, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop5.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            elif not checkBookExists(mem_7_acc_ent.get()):
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

                back = Button(pop4, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop4.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if not checkDateFormat(mem_7_returnDate_ent.get()):
                global pop6
                pop6 = Toplevel(self)
                pop6.title("Error!")
                pop6.geometry("600x400")
                pop6.config(bg="#C53A5A")

                pop6_label1 = Label(pop6, text="Error!", font=controller.normal_font)
                pop6_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop6_label2 = Label(pop6, text= "Invalid date format", font=controller.normal_font)      #backend determine which error msg
                pop6_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop6, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop6, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop6.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            if not checkBookBorrowed(mem_7_acc_ent.get()):
                global pop8
                pop8 = Toplevel(self)
                pop8.title("Error!")
                pop8.geometry("600x400")
                pop8.config(bg="#C53A5A")

                pop8_label1 = Label(pop8, text="Error!", font=controller.normal_font)
                pop8_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop8_label2 = Label(pop8, text= "Book has not been borrowed", font=controller.normal_font)      #backend determine which error msg
                pop8_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop8, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop8, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop8.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            
            mycursor = mydb.cursor()
            mycursor.execute("SELECT CAST(loanStart AS DATE) FROM Loans WHERE accessionNo = %s AND loanReturn IS NULL", (mem_7_acc_ent.get(),))
            loanStartDate = mycursor.fetchone()[0]
            if convert_to_date(mem_7_returnDate_ent.get()) < loanStartDate:
                global pop7
                pop7 = Toplevel(self)
                pop7.title("Error!")
                pop7.geometry("600x400")
                pop7.config(bg="#C53A5A")

                pop7_label1 = Label(pop7, text="Error!", font=controller.normal_font)
                pop7_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop7_label2 = Label(pop7, text= "Invalid return date", font=controller.normal_font)      #backend determine which error msg
                pop7_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop7, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop7, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop7.destroy()])
                back.place(relx=0.5, rely=0.75, anchor=CENTER)
                return
            global pop1
            pop1 = Toplevel(self)
            pop1.title("Confirm return details")
            pop1.geometry("600x400")
            pop1.config(bg="#3ac5a5")

            def get_accession_number():
                return mem_7_acc_ent.get()

            def get_title():
                acc_no = mem_7_acc_ent.get()
                mycursor.execute("SELECT title FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                return result

            def get_memID():
                mem_id = getMemReturningBook(mem_7_acc_ent.get())
                return mem_id
            
            def get_memName():
                mem_id = get_memID()
                mycursor.execute("SELECT lName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                result = mycursor.fetchone()[0]
                if result != None:
                    mycursor.execute("SELECT concat(fName, ' ', lName) FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                else:
                    mycursor.execute("SELECT fName FROM LibMembers WHERE membershipID = %s", (mem_id,))
                    final_result = mycursor.fetchone()[0]
                return final_result

            def get_returnDate():
                return mem_7_returnDate_ent.get()
            
            def get_fineAmt():
                if (convert_to_date(get_returnDate()) > getLoanDueDate(mem_7_acc_ent.get())):
                    return_date = convert_to_date(get_returnDate())
                    mycursor.execute("SELECT DATEDIFF(%s, %s)", (return_date, getLoanDueDate(mem_7_acc_ent.get())))
                    dateDiff = mycursor.fetchone()[0]
                    return dateDiff
                else:
                    return 0

            pop1_label_main = Label(pop1, text="Confirm Return Details To Be Correct", font=controller.normal_font)
            pop1_label_main.place(relx=0.5, rely=0.1, anchor=CENTER)
            pop1_label_accnum = Label(pop1, text= get_accession_number(), font=controller.normal_font)  ##quotation marks are to test
            pop1_label_accnum.place(relx=0.5, rely=0.2, anchor=CENTER)
            pop1_label_title = Label(pop1, text= get_title(), font=controller.normal_font)
            pop1_label_title.place(relx=0.5, rely=0.3, anchor=CENTER)
            pop1_label_memID = Label(pop1, text= get_memID(), font=controller.normal_font)
            pop1_label_memID.place(relx=0.5, rely=0.4, anchor=CENTER)
            pop1_label_memName = Label(pop1, text= get_memName(), font=controller.normal_font)
            pop1_label_memName.place(relx=0.5, rely=0.5, anchor=CENTER)
            pop1_label_returnDate = Label(pop1, text= get_returnDate(), font=controller.normal_font)
            pop1_label_returnDate.place(relx=0.5, rely=0.6, anchor=CENTER)
            pop1_label_fineAmt = Label(pop1, text= "$" + str(get_fineAmt()), font=controller.normal_font)
            pop1_label_fineAmt.place(relx=0.5, rely=0.7, anchor=CENTER)

            return_frame = Frame(pop1, bg="#3ac5a5")
            return_frame.place(anchor=CENTER)

            confirm = Button(pop1, text="Confirm Return", font=controller.normal_font, command=lambda: [return_book(), pop1.destroy()])  ##withdraw or error
            confirm.place(relx=0.33, rely=0.85, anchor=CENTER)

            back = Button(pop1, text="Back to Return function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop1.destroy()])
            back.place(relx=0.66, rely=0.85, anchor=CENTER)

        def return_book():
            return_date = convert_to_date(mem_7_returnDate_ent.get())
            if (return_date > getLoanDueDate(mem_7_acc_ent.get())):
                mycursor=mydb.cursor(buffered=True)
                mycursor.execute("SELECT DATEDIFF(%s, %s)", (return_date, getLoanDueDate(mem_7_acc_ent.get())))
                dateDiff = mycursor.fetchone()[0]
                mycursor.execute("SELECT paymentAmt FROM Fines WHERE membershipID = %s", (getMemReturningBook(mem_7_acc_ent.get()),))
                existingFine = mycursor.fetchone()[0]
                sql = "UPDATE Fines SET paymentAmt = %s WHERE membershipID = %s"
                val = (dateDiff + existingFine, getMemReturningBook(mem_7_acc_ent.get()))
                mycursor.execute(sql, val)
                mydb.commit()
                msg = "Book returned successfully but has incurred fines"
            else:
                msg = "Book returned successfully"

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("UPDATE Loans SET loanReturn = %s WHERE accessionNo = %s AND \
                membershipID = %s", (return_date, mem_7_acc_ent.get(), getMemReturningBook(mem_7_acc_ent.get())))
            mydb.commit()
            
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

            back = Button(pop3, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop3.destroy()])
            back.place(relx=0.5, rely=0.75, anchor=CENTER)
            ##insert code here to indicate return book is successful

        # def return_or_error():
        #     error_string = get_error()
            
        #     if error_string == "":   #backend check if returned book has fines
        #         return return_book()            #backend return func
        #     else:
        #         global pop2
        #         pop2 = Toplevel(self)
        #         pop2.title("Error!")
        #         pop2.geometry("600x400")
        #         pop2.config(bg="#C53A5A")

        #         pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
        #         pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
        #         pop2_label2 = Label(pop2, text= "Book Returned Successfully but has Fines", font=controller.normal_font)   
        #         pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

        #         error_frame = Frame(pop2, bg="#C53A5A")
        #         error_frame.place(anchor=CENTER)

        #         back = Button(pop2, text="Back to Return Function", font=controller.normal_font, command=lambda: [controller.show_frame("Loa_7_Return"), pop2.destroy()])
        #         back.place(relx=0.5, rely=0.75, anchor=CENTER)

        #         return return_book()     #book is returned either way

        #buttons
        mem_7_returnButton = Button(self, text="Return book", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=confirm_popup)
        mem_7_returnButton.place(relx=0.25, rely=0.8, anchor=CENTER)
        #mem_7_returnButton.grid(row=80, column=2, padx=10, pady=10)

        mem_7_menuButton = Button(self, text="Back to Loans Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=lambda: controller.show_frame("LoanMenu"))
        mem_7_menuButton.place(relx=0.5, rely=0.8, anchor=CENTER)
        #mem_7_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font,
        bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.8, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

