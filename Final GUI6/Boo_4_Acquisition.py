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

class Boo_4_Acquisition(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "boobg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller
       
        # instruction 
        mem_1_instruction = Label(self, text = "For New Book Acquisition, please enter the required information below", font=controller.title_font, bg="#b1b8c0")
        mem_1_instruction.place(relx=0.5, rely=0.1, anchor=CENTER)
        #mem_1_instruction.grid(row=1, column=1, sticky="W", pady=5)


        # labels 
        mem_4_acc_lab = Label(self, text = "Accession number", font=controller.normal_font, bg="#b1b8c0")
        mem_4_acc_lab.place(relx=0.33, rely=0.18, anchor=CENTER)
        #mem_4_acc_lab.grid(row=5, column=0, sticky="E", padx=5, pady=10)

        mem_4_title_lab = Label(self, text = "Title", font=controller.normal_font, bg="#b1b8c0")
        mem_4_title_lab.place(relx=0.33, rely=0.26, anchor=CENTER)
        #mem_4_title_lab.grid(row=7, column=0, sticky="E", padx=5, pady=10)

        mem_4_author1_lab = Label(self, text = "Author 1", font=controller.normal_font, bg="#b1b8c0")
        mem_4_author1_lab.place(relx=0.33, rely=0.34, anchor=CENTER)
        #mem_4_author_lab.grid(row=9, column=0, sticky="E", padx=5, pady=10)

        mem_4_author2_lab = Label(self, text = "Author 2", font=controller.normal_font, bg="#b1b8c0")
        mem_4_author2_lab.place(relx=0.33, rely=0.42, anchor=CENTER)

        mem_4_author3_lab = Label(self, text = "Author 3", font=controller.normal_font, bg="#b1b8c0")
        mem_4_author3_lab.place(relx=0.33, rely=0.5, anchor=CENTER)

        mem_4_ISBN_lab = Label(self, text = "ISBN", font=controller.normal_font, bg="#b1b8c0")
        mem_4_ISBN_lab.place(relx=0.33, rely=0.58, anchor=CENTER)
        #mem_4_ISBN_lab.grid(row=11, column=0, sticky="E", padx=5, pady=10)

        mem_4_publisher_lab = Label(self, text = "Publisher", font=controller.normal_font, bg="#b1b8c0")
        mem_4_publisher_lab.place(relx=0.33, rely=0.64, anchor=CENTER)
        #mem_4_publisher_lab.grid(row=13, column=0, sticky="E", padx=5, pady=10)

        mem_4_publishyr_lab = Label(self, text = "Publication Year", font=controller.normal_font, bg="#b1b8c0")
        mem_4_publishyr_lab.place(relx=0.33, rely=0.72, anchor=CENTER)
        #mem_4_publishyr_lab.grid(row=15, column=0, sticky="E", padx=5, pady=10)


        # entry box
        mem_4_acc_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_acc_ent.place(relx=0.66, rely=0.18, anchor=CENTER)
        #mem_4_acc_ent.grid(row=5, column=1, padx=5, pady=10)

        mem_4_title_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_title_ent.place(relx=0.66, rely=0.26, anchor=CENTER)
        #mem_4_title_ent.grid(row=7, column=1, padx=5, pady=10)

        mem_4_author1_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_author1_ent.place(relx=0.66, rely=0.34, anchor=CENTER)
        #mem_4_author1_ent.grid(row=9, column=1, padx=5, pady=10)

        mem_4_author2_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_author2_ent.place(relx=0.66, rely=0.42, anchor=CENTER)
        #mem_4_author2_ent.grid(row=9, column=1, padx=5, pady=10)

        mem_4_author3_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_author3_ent.place(relx=0.66, rely=0.5, anchor=CENTER)
        #mem_4_author3_ent.grid(row=9, column=1, padx=5, pady=10)

        mem_4_ISBN_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_ISBN_ent.place(relx=0.66, rely=0.58, anchor=CENTER)
        #mem_4_ISBN_ent.grid(row=11, column=1, padx=5, pady=10)

        mem_4_publisher_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_publisher_ent.place(relx=0.66, rely=0.66, anchor=CENTER)
        #mem_4_publisher_ent.grid(row=13, column=1, padx=5, pady=10)

        mem_4_publishyr_ent = Entry(self, width=30, fg="black", font=controller.normal_font)
        mem_4_publishyr_ent.place(relx=0.66, rely=0.74, anchor=CENTER)
        #mem_4_publishyr_ent.grid(row=15, column=1, padx=5, pady=10)

        def checkBookExists(accession_no):
            mycursor.execute("SELECT accessionNo FROM Books WHERE accessionNo = %s", (accession_no,))
            result = mycursor.fetchall()
            if len(result) == 0: 
                return False
            return True

        def invalidYear(year):
            if (len(year) != 4) or (not year.isdigit()):
                return True
            return False

        def invalidAccessionNo(accession_no):
            if len(accession_no) > 5:
                return True
            return False

        def get_error():
            err = ""
            if mem_4_acc_ent.get() == "" or mem_4_title_ent.get() == "":
                err += "Missing mandatory fields (Accession number, title);"
                return err[:-1]
            if invalidAccessionNo(mem_4_acc_ent.get()):
                err += "Invalid accession number entered;"
            elif checkBookExists(mem_4_acc_ent.get()):
                err += "Book already exists: Book accession number is already in use;"
            if invalidYear(mem_4_publishyr_ent.get()):
                err += "Invalid publication year entered;"  
            err = err[:-1]
            return err

        #Button functions
        def which_popup(): 
            error_string = get_error()

            if error_string != "":
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg = "#C53A5A")

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop2_label2 = Label(pop2, text=error_string, font=controller.normal_font)
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                error_frame = Frame(pop2, bg = "#C53A5A")
                error_frame.place(anchor=CENTER)

                yes = Button(pop2, text="Back to Acquisition Function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_4_Acquisition"), pop2.destroy()])
                yes.place(relx=0.5, rely=0.75, anchor=CENTER)


            else:
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Success!")
                pop1.geometry("600x400")
                pop1.config(bg="#3ac5a5")

                pop1_label1 = Label(pop1, text="Success!", font=controller.normal_font)
                pop1_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop1_label2 = Label(pop1, text="New book added to library.", font=controller.normal_font)
                pop1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)
                
                success_frame = Frame(pop1, bg="#3ac5a5")
                success_frame.place(anchor=CENTER)

                yes = Button(pop1, text="Back to Acquisition function", font=controller.normal_font, command=lambda: [controller.show_frame("Boo_4_Acquisition"), pop1.destroy()])
                yes.place(relx=0.5, rely=0.75, anchor=CENTER)

                sql = "INSERT INTO Books (accessionNo, title, author1, author2, author3, ISBN, publisher, publicationYear) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (mem_4_acc_ent.get(), mem_4_title_ent.get(), mem_4_author1_ent.get(), mem_4_author2_ent.get(), mem_4_author3_ent.get(), mem_4_ISBN_ent.get(), mem_4_publisher_ent.get(), mem_4_publishyr_ent.get())
                mycursor.execute(sql, val)
                mydb.commit()


        #Buttons
        mem_4_addButton = Button(self, text="Add new book", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0",
        command=which_popup)
        mem_4_addButton.place(relx=0.25, rely=0.85, anchor=CENTER)
        #mem_4_addButton.grid(row=80, column=2, padx=10, pady=10)

        mem_4_backButton = Button(self, text="Back to Books Menu", padx=10, pady=10, font=controller.normal_font, bg="#b1b8c0", 
        command=lambda: controller.show_frame("BookMenu"))
        mem_4_backButton.place(relx=0.5, rely=0.85, anchor=CENTER)
        #mem_4_backButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, font=controller.normal_font, fg="white", bg="black", 
        command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.85, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)

