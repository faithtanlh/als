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


class Mem_1_Creation(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg_path = "membg.png"
        self.bg = PhotoImage(file=bg_path)
        label_bkgr = Label(self, image=self.bg)
        label_bkgr.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.controller = controller

        # instruction
        mem_1_instruction = Label(self, text = "To create member, please enter the required information below",font=controller.title_font, bg="#b1b8c0")
        mem_1_instruction.place(relx=0.5, rely=0.1, anchor=CENTER)
        #mem_1_instruction.grid(row=1, column=1, sticky="W", pady=5)
        
        # labels 
        mem_1_id_lab = Label(self, text = "Membership ID", font=controller.normal_font, bg="#b1b8c0")
        mem_1_id_lab.place(relx=0.33, rely=0.2, anchor=CENTER)
        #mem_1_id_lab.grid(row=5, column=0,  sticky="E", padx=20, pady=3)

        mem_1_firstname_lab = Label(self, text = "First Name", font=controller.normal_font, bg="#b1b8c0")
        mem_1_firstname_lab.place(relx=0.33, rely=0.3, anchor=CENTER)
        #mem_1_firstname_lab.grid(row=7, column=0, sticky="E", padx=20, pady=3)

        mem_1_lastname_lab = Label(self, text = "Last Name", font=controller.normal_font, bg="#b1b8c0")
        mem_1_lastname_lab.place(relx=0.33, rely=0.4, anchor=CENTER)
        #mem_1_lastname_lab.grid(row=9, column=0, sticky="E", padx=20, pady=3)

        mem_1_faculty_lab = Label(self, text = "Faculty", font=controller.normal_font, bg="#b1b8c0")
        mem_1_faculty_lab.place(relx=0.33, rely=0.5, anchor=CENTER)
        #mem_1_faculty_lab.grid(row=11, column=0, sticky="E", padx=20, pady=3)

        mem_1_phone_num_lab = Label(self, text = "Phone Number", font=controller.normal_font, bg="#b1b8c0")
        mem_1_phone_num_lab.place(relx=0.33, rely=0.6, anchor=CENTER)
        #mem_1_phone_num_lab.grid(row=13, column=0, sticky="E", padx=20, pady=3)

        mem_1_email_add_lab = Label(self, text = "Email Address", font=controller.normal_font, bg="#b1b8c0")
        mem_1_email_add_lab.place(relx=0.33, rely=0.7, anchor=CENTER)
        #mem_1_email_add_lab.grid(row=15, column=0, sticky="E", padx=20, pady=3)
        


        # entry box
        mem_1_id_ent = Entry(self, width=30, font=controller.normal_font)
        mem_1_id_ent.place(relx=0.66, rely=0.2, anchor=CENTER)
        #mem_1_id_ent.grid(row=5, column=1, padx=5, pady=3) 
        
        mem_1_firstname_ent = Entry(self, width=30, font=controller.normal_font)
        mem_1_firstname_ent.place(relx=0.66, rely=0.3, anchor=CENTER)
        #mem_1_firstname_ent.grid(row=7, column=1, padx=5, pady=3)

        mem_1_lastname_ent = Entry(self, width=30, font=controller.normal_font)
        mem_1_lastname_ent.place(relx=0.66, rely=0.4, anchor=CENTER)
        
        OPTIONS = ["Science", "Business", "Law", "FASS", "Engineering", "Medicine", "Computing", "Dentistry", "Design & Engineering", "Others"]
        mem_1_faculty_ent = StringVar(self)
        mem_1_faculty_ent.set("") #default value

        w = OptionMenu(self, mem_1_faculty_ent, *OPTIONS)
        w.config(width=25, font=controller.normal_font)
        w.place(relx=0.66, rely=0.5, anchor=CENTER) 
        
        #mem_1_faculty_ent = Entry(self, width=30, font=controller.normal_font) 
        #mem_1_faculty_ent.place(relx=0.66, rely=0.5, anchor=CENTER)
        #mem_1_faculty_ent.grid(row=11, column=1, padx=5, pady=3)R)
        #mem_1_faculty_ent.grid(row=11, column=1, padx=5, pady=3)

        mem_1_phone_num_ent = Entry(self, width=30, font=controller.normal_font)
        mem_1_phone_num_ent.place(relx=0.66, rely=0.6, anchor=CENTER)
        #mem_1_phone_num_ent.grid(row=13, column=1, padx=5, pady=3)

        mem_1_email_add_ent = Entry(self, width=30, font=controller.normal_font)
        mem_1_email_add_ent.place(relx=0.66, rely=0.7, anchor=CENTER)
        #mem_1_email_add_ent.grid(row=15, column=1, padx=5, pady=3)


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

        def invalidMemID(mem_id):
            ref_alphabets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if mem_id == "":
                return False
            elif (len(mem_id) > 8) or(mem_id[0] not in ref_alphabets) or (mem_id[-1] not in ref_alphabets) or \
                (mem_id[1:-1].isdigit() == False):
                return True
            else:
                return False

        def invalidPhoneNo(phoneNo):
            if phoneNo == "":
                return False
            if (len(phoneNo) != 8) or (not phoneNo.isdigit()):
                return True
            else:
                return False

        def get_error():
            ##missing mandatory fields
            err = ""
            if (mem_1_id_ent.get() == "") or (mem_1_firstname_ent.get() == "") or (mem_1_email_add_ent.get() == ""):
                err += "Missing mandatory fields (Membership ID, first name, email);"
            ##invalid member ID
            if invalidMemID(mem_1_id_ent.get()) or invalidPhoneNo(mem_1_phone_num_ent.get()):
                if invalidMemID(mem_1_id_ent.get()):
                    err += "\nInvalid Membership ID entered;"
                if invalidPhoneNo(mem_1_phone_num_ent.get()):
                    err += "\nInvalid phone number entered;"
            ##memID or email in use
            else:
                if memID_used(mem_1_id_ent.get()) and email_used(mem_1_email_add_ent.get()):
                    err += "\nMember already exists: Membership ID and email are currently in use;"
                elif memID_used(mem_1_id_ent.get()):
                    err += "\nMembership ID is currently in use;"
                elif email_used(mem_1_email_add_ent.get()):
                    err += "\nEmail is currently in use;"
            err = err[:-1]
            return err

        def which_popup(): 
            error_string = get_error()

            if error_string != "":
                global pop2
                pop2 = Toplevel(self)
                pop2.title("Error!")
                pop2.geometry("600x400")
                pop2.config(bg="#C53A5A")

                error_frame = Frame(pop2, bg="#C53A5A")
                error_frame.place(anchor=CENTER)

                pop2_label1 = Label(pop2, text="Error!", font=controller.normal_font)
                pop2_label1.place(relx = 0.5, rely = 0.25, anchor = CENTER)
                pop2_label2 = Label(pop2, text=error_string, font=controller.normal_font)
                pop2_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                yes = Button(pop2, text="Back to Create Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_1_Creation"), pop2.destroy()])
                yes.place(relx = 0.5, rely = 0.75, anchor = CENTER)

            else:
                global pop1
                pop1 = Toplevel(self)
                pop1.title("Success!")
                pop1.geometry("600x400")
                pop1.config(bg="#3ac5a5")

                success_frame = Frame(pop1, bg="#3ac5a5")
                success_frame.place(anchor=CENTER)

                pop1_label1 = Label(pop1, text="Success!", font=controller.normal_font)
                pop1_label1.place(relx=0.5, rely=0.25, anchor=CENTER)
                pop1_label2 = Label(pop1, text="ALS membership created.", font=controller.normal_font)
                pop1_label2.place(relx=0.5, rely=0.5, anchor=CENTER)

                yes = Button(pop1, text="Back to Create Function", font=controller.normal_font, command=lambda: [controller.show_frame("Mem_1_Creation"), pop1.destroy()])
                yes.place(relx=0.5, rely=0.75, anchor=CENTER)

                sql = "INSERT INTO LibMembers (membershipID, fName, lName, faculty, phoneNo, eMail) VALUES \
                    (%s, %s, %s, %s, %s, %s)"
                val = (mem_1_id_ent.get(), mem_1_firstname_ent.get(), mem_1_lastname_ent.get(), mem_1_faculty_ent.get(), mem_1_phone_num_ent.get(), mem_1_email_add_ent.get())
                mycursor.execute(sql, val)
                sql = "INSERT INTO Fines (paymentDate, paymentAmt, membershipID) VALUES (%s, %s, %s)"
                val = (None, 0, mem_1_id_ent.get())
                mycursor.execute(sql, val)
                mydb.commit()


        mem_1_createButton = Button(self, text="Create Member", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=which_popup)
        mem_1_createButton.place(relx=0.25, rely=0.85, anchor=CENTER)
        #mem_1_createButton.grid(row=80, column=2, padx=10, pady=10)

        mem_1_backButton = Button(self, text="Back to Membership Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="#b1b8c0", command=lambda: controller.show_frame("MembershipMenu"))
        mem_1_backButton.place(relx=0.5, rely=0.85, anchor=CENTER)
        #mem_1_backButton.grid(row=80, column=1, sticky="E", padx=10, pady=10)

        mainmenuButton = Button(self, text="Back to Main Menu", padx=10, pady=10, 
        font=controller.normal_font, bg="black", fg="white", command=lambda: controller.show_frame("MainMenu"))
        mainmenuButton.place(relx=0.75, rely=0.85, anchor=CENTER)
        #mainmenuButton.grid(row=80, column=0, sticky="E", padx=10, pady=10)


