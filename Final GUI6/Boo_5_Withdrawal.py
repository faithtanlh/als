from tkinter import *
from BT2102_ALS_functions import * 
import mysql.connector
from SQLpassword import get_password

my_password = get_password()
mydb = mysql.connector.connect(
host = "localhost", 
user = "root", 
passwd = my_password, 
database = "libals")

mycursor = mydb.cursor()


class Boo_5_Withdrawal(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "boobg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.controller = controller
       
        #instruction 
        mem_5_instruction = Label(self, text = "To Remove Outdated Books, Please Enter Required Information Below:", font=controller.title_font, bg="#b1b8c0")
        mem_5_instruction.place(relx=0.5, rely=0.25, anchor=CENTER)
        #mem_5_instruction.grid(row=1, column=1, sticky="W", pady=5)

        #labels
        mem_5_acc_lab = Label(self, text = "Accession number", font=controller.normal_font, bg="#b1b8c0")
        mem_5_acc_lab.place(relx=0.33, rely=0.5, anchor=CENTER)
        #mem_5_acc_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        #entry box
        mem_5_acc_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_5_acc_ent.place(relx=0.66, rely=0.5, anchor=CENTER)
        #mem_5_acc_ent.grid(row=5, column=1, padx=5, pady=10)

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

        #button functions
        def confirm_popup():
            if invalidAccessionNo(mem_5_acc_ent.get()):
                global pop5
                pop5 = Toplevel(self)
                pop5.title("Error!")
                pop5.geometry("600x400")
                pop5.config(bg = "#C53A5A")

                pop5_label1 = Label(pop5, text="Error!", font=controller.normal_font)
                pop5_label1.place(relx=0.5 ,rely=0.25, anchor=CENTER)
                pop5_label2 = Label(pop5, text= "Invalid accession number", font=controller.normal_font)      #backend determine which error msg
                pop5_label2.place(relx=0.5 ,rely=0.5, anchor=CENTER)

                error_frame = Frame(pop5, bg = "#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop5, text="Back to Withdrawal Function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_5_Withdrawal"), pop5.destroy()])
                back.place(relx=0.5 ,rely=0.75, anchor=CENTER)
                return
            elif not checkBookExists(mem_5_acc_ent.get()):
                global pop4
                pop4 = Toplevel(self)
                pop4.title("Error!")
                pop4.geometry("600x400")
                pop4.config(bg = "#C53A5A")

                pop4_label1 = Label(pop4, text="Error!", font=controller.normal_font)
                pop4_label1.place(relx=0.5 ,rely=0.25, anchor=CENTER)
                pop4_label2 = Label(pop4, text= "Book does not exist", font=controller.normal_font)      #backend determine which error msg
                pop4_label2.place(relx=0.5 ,rely=0.5, anchor=CENTER)

                error_frame = Frame(pop4, bg = "#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop4, text="Back to Withdrawal Function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_5_Withdrawal"), pop4.destroy()])
                back.place(relx=0.5 ,rely=0.75, anchor=CENTER)
                return

            global pop1
            pop1 = Toplevel(self)
            pop1.title("Confirm withdrawal details")
            pop1.geometry("600x400")
            pop1.config(bg="#3ac5a5")

            def get_accession_number():
                return mem_5_acc_ent.get()

            def get_title():
                acc_no = mem_5_acc_ent.get()
                mycursor.execute("SELECT title FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                return result

            def get_authors():
                acc_no = mem_5_acc_ent.get()
                mycursor.execute("SELECT author1, author2, author3 FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()
                final_result = ""
                for i in result:
                    if i != None:
                        final_result += i + ";"
                return final_result

            def get_ISBN():
                acc_no = mem_5_acc_ent.get()
                mycursor.execute("SELECT ISBN FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                if result == None:
                    return ""
                return result
            
            def get_publisher():
                acc_no = mem_5_acc_ent.get()
                mycursor.execute("SELECT publisher FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                if result == None:
                    return ""
                return result

            def get_year():
                acc_no = mem_5_acc_ent.get()
                mycursor.execute("SELECT publicationYear FROM Books WHERE accessionNo = %s", (acc_no,))
                result = mycursor.fetchone()[0]
                if result == None:
                    return ""
                return result

            pop1_label_main = Label(pop1, text="Please Confirm Details to be Correct", font=controller.normal_font)
            pop1_label_main.place(relx=0.5, rely=0.1, anchor=CENTER)

            pop1_label_accnum = Label(pop1, text= get_accession_number(), font=controller.normal_font)  ##quotation marks are to test
            pop1_label_accnum.place(relx=0.5, rely=0.2, anchor=CENTER)
            pop1_label_title = Label(pop1, text= get_title(), font=controller.normal_font)
            pop1_label_title.place(relx=0.5, rely=0.3, anchor=CENTER)
            pop1_label_authors = Label(pop1, text= get_authors(), font=controller.normal_font)
            pop1_label_authors.place(relx=0.5, rely=0.4, anchor=CENTER)
            pop1_label_ISBN = Label(pop1, text= get_ISBN(), font=controller.normal_font)
            pop1_label_ISBN.place(relx=0.5, rely=0.5, anchor=CENTER)
            pop1_label_publisher = Label(pop1, text= get_publisher(), font=controller.normal_font)
            pop1_label_publisher.place(relx=0.5, rely=0.6, anchor=CENTER)
            pop1_label_year = Label(pop1, text= get_year(), font=controller.normal_font)
            pop1_label_year.place(relx=0.5, rely=0.7, anchor=CENTER)

            withdraw_frame = Frame(pop1, bg="#3ac5a5")
            withdraw_frame.place(anchor=CENTER)

            confirm = Button(pop1, text="Confirm Withdrawal", font=controller.normal_font, command=lambda: [withdraw_or_error(), pop1.destroy()])  ##withdraw or error
            confirm.place(relx=0.33, rely=0.8, anchor=CENTER)

            back = Button(pop1, text="Back to withdrawal function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_5_Withdrawal"), pop1.destroy()])
            back.place(relx=0.66, rely=0.8, anchor=CENTER)

        def checkBookBorrowed(accession_no):
            mycursor.execute("SELECT accessionNo FROM Loans WHERE accessionNo = %s AND \
                loanReturn IS NULL", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def checkReserved(accession_no):
            mycursor.execute("SELECT accessionNo FROM Reservations WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0:
                return False
            return True

        def get_error():
            err = ""
            if not checkBookExists(mem_5_acc_ent.get()):
                err += "\nBook does not exist;"      
            if checkBookBorrowed(mem_5_acc_ent.get()):
                err += "\nBook is currently on loan;"
            if checkReserved(mem_5_acc_ent.get()):
                err += "\nBook is currently reserved;"
            err = err[:-1]
            return err

        def withdraw_book():
            mycursor.execute("DELETE FROM Books WHERE accessionNo = %s", (mem_5_acc_ent.get(),))
            mydb.commit()
            global pop3
            pop3 = Toplevel(self)
            pop3.title("Success!")
            pop3.geometry("600x400")
            pop3.config(bg="#3ac5a5")

            pop3_label1 = Label(pop3, text="Success!", font=controller.normal_font)
            pop3_label1.place(relx=0.5 ,rely=0.25, anchor=CENTER)
            pop3_label2 = Label(pop3, text="Book has been withdrawn.", font=controller.normal_font)
            pop3_label2.place(relx=0.5 ,rely=0.5, anchor=CENTER)

            success_frame = Frame(pop3, bg="#3ac5a5")
            success_frame.place(anchor=CENTER)

            back = Button(pop3, text="Back to Withdrawal Function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_5_Withdrawal"), pop3.destroy()])
            back.place(relx=0.5 ,rely=0.75, anchor=CENTER)
            ##insert GUI code here to indicate success of withdrawal

        def withdraw_or_error():
            error_string = get_error()

            if error_string == "":   #backend check if book is on loan or reserve
                return withdraw_book()            #backend withdraw func
            else:
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg = "#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5 ,rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text= error_string, font=controller.normal_font)      #backend determine which error msg
                pop2_label2.place(relx=0.5 ,rely=0.5, anchor=CENTER)

                error_frame = Frame(pop2, bg = "#C53A5A")
                error_frame.place(anchor=CENTER)

                back = Button(pop2, text="Back to Withdrawal Function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_5_Withdrawal"), pop2.destroy()])
                back.place(relx=0.5 ,rely=0.75, anchor=CENTER)

        #buttons
        mem_5_withdrawButton = Button(self, text="Withdraw book", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0", 
        command=confirm_popup)
        mem_5_withdrawButton.place(relx=0.25, rely=0.75, anchor=CENTER)
        #mem_5_withdrawButton.grid(row=80, column=2, padx=10, pady=10)

        mem_5_menuButton = Button(self, text="Back to Books Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="#b1b8c0", command=lambda: controller.show_frame("BookMenu"))
        mem_5_menuButton.place(relx=0.5, rely=0.75, anchor=CENTER)
        #mem_5_menuButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, 
        bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.75, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)


